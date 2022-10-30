import os
import ydb
import random
from typing import Collection

from logging_decorator import logger
from set_orm import SetORM
from user_orm import UserORM
from abstract_base import AbstractBase, UserDoesntExistInDB, SetDoesntExistInDB, TermDoesntExistInDB


class Database(AbstractBase):

    def __init__(self):
        self.driver = ydb.Driver(
            endpoint=os.getenv('YDB_ENDPOINT'),
            database=os.getenv('YDB_DATABASE'),
            credentials=ydb.construct_credentials_from_environ(),
        )
        self.driver.wait(fail_fast=True, timeout=5)
        self.pool = ydb.SessionPool(self.driver)

    @logger
    def get_user_info(self, user_id: str) -> UserORM:
        def select(session):
            return session.transaction().execute(
                'SELECT `id`, `state`, `set_id`, `term_id`, `definition_id`, `sample_id`, `card_id` FROM `users` WHERE `id` == "{}";'.format(user_id),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)

        if len(result[0].rows) == 0:
            raise UserDoesntExistInDB

        return UserORM(
            id=user_id,
            state=result[0].rows[0].state,
            set_id=result[0].rows[0].set_id,
            term_id=result[0].rows[0].term_id,
            definition_id=result[0].rows[0].definition_id,
            sample_id=result[0].rows[0].sample_id,
            card_id=result[0].rows[0].card_id,
        )

    @logger
    def set_user_info(self, user: UserORM) -> None:
        def upsert(session):
            return session.transaction().execute(
                'UPSERT INTO `users` (`id`, `state`, `set_id`, `term_id`, `definition_id`, `sample_id`, `card_id`) VALUES ("{}", {}, {}, {}, {}, {}, {});'.format(
                    user.id,
                    user.state,
                    user.set_id,
                    user.term_id,
                    user.definition_id,
                    user.sample_id,
                    user.card_id,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        self.pool.retry_operation_sync(upsert)

    @logger
    def get_user_sets(self, user_id: str) -> Collection[SetORM]:
        def select(session):
            return session.transaction().execute(
                'SELECT `id`, `origin_set_id`, `name` FROM `sets` WHERE `user_id` == "{}";'.format(user_id),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)
        return [SetORM(id=e.id, origin_set_id=e.origin_set_id, name=e.name.decode('utf-8')) for e in result[0].rows]

    @logger
    def get_set_by_id(self, set_id: int) -> SetORM:
        def select(session):
            return session.transaction().execute(
                'SELECT `id`, `name`, `origin_set_id` FROM `sets` WHERE `id` == {};'.format(set_id),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)
        if len(result[0].rows) == 0:
            raise SetDoesntExistInDB

        return SetORM(
            id=set_id,
            name=result[0].rows[0].name.decode('utf-8'),
            origin_set_id=result[0].rows[0].origin_set_id,
        )

    @logger
    def get_user_set_by_id(self, user_id: str, set_id: int) -> SetORM:
        def select(session):
            return session.transaction().execute(
                'SELECT `id`, `name`, `origin_set_id` FROM `sets` WHERE `id` == {} and `user_id` == "{}";'.format(
                    set_id,
                    user_id,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)
        if len(result[0].rows) == 0:
            raise SetDoesntExistInDB

        return SetORM(
            id=set_id,
            name=result[0].rows[0].name.decode('utf-8'),
            origin_set_id=result[0].rows[0].origin_set_id,
        )

    @logger
    def copy_set(self, user_id: str, set_name: str, set_id: int) -> None:
        def upsert(session):
            return session.transaction().execute(
                'UPSERT INTO `sets` (`id`, `user_id`, `origin_set_id`, `name`) VALUES ({}, "{}", {}, "{}");'.format(
                    int(user_id) * 1000 + random.randint(0, 999),
                    user_id,
                    set_id,
                    set_name,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        self.pool.retry_operation_sync(upsert)

    @logger
    def create_set(self, user_id: str, set_name: str) -> None:
        def upsert(session):
            set_id = int(user_id) * 1000 + random.randint(0, 999)
            return session.transaction().execute(
                'UPSERT INTO `sets` (`id`, `user_id`, `origin_set_id`, `name`) VALUES ({}, "{}", {}, "{}");'.format(
                    set_id,
                    user_id,
                    set_id,
                    set_name,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        self.pool.retry_operation_sync(upsert)

    @logger
    def disconnect_set_and_user(self, set_id: int) -> None:
        def upsert(session):
            return session.transaction().execute(
                'UPSERT INTO `sets` (`id`, `user_id`) VALUES ({}, "")'.format(set_id),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        self.pool.retry_operation_sync(upsert)

    @logger
    def get_count_of_cards(self, set_id: int) -> int:
        def select(session):
            return session.transaction().execute(
                'SELECT COUNT(*) as `count` FROM `cards` WHERE `set_id` == {};'.format(set_id),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)

        return result[0].rows[0].count

    @logger
    def get_term_id(self, term: str) -> int:
        def select(session):
            return session.transaction().execute(
                'SELECT `id` FROM `terms` WHERE `term` == "{}";'.format(term),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)

        if len(result[0].rows) == 0:
            raise TermDoesntExistInDB

        return result[0].rows[0].id

    @logger
    def create_term(self, set_id: int, term: str) -> int:
        term_id = set_id * 1000000 + random.randint(0, 999999)

        def upsert(session):
            return session.transaction().execute(
                'UPSERT INTO `terms` (`id`, `term`) VALUES ({}, "{}");'.format(term_id, term),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        self.pool.retry_operation_sync(upsert)

        return term_id
