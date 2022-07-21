import os
import ydb
from typing import Iterable

from logging_decorator import logger
from set_orm import SetORM
from user_orm import UserORM
from abstract_base import AbstractBase, UserDoesntExistInDB


class Database(AbstractBase):
    def __init__(self):
        self.driver = ydb.Driver(endpoint=os.getenv('YDB_ENDPOINT'), database=os.getenv('YDB_DATABASE'))
        self.driver.wait(fail_fast=True, timeout=5)
        self.pool = ydb.SessionPool(self.driver)

    @logger
    def get_user_info(self, user_id: str) -> UserORM:
        def select(session):
            return session.transaction().execute(
                'SELECT `id`, `state`, `data` FROM `users` WHERE `id` == "{}";'.format(user_id),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)
        if len(result[0]) == 0:
            raise UserDoesntExistInDB

        orm = UserORM(
            id=user_id,
            state=result[0].rows[0].state,
            data=result[0].rows[0].data,
        )
        return orm

    @logger
    def set_user_info(self, user: UserORM) -> None:
        pass

    @logger
    def get_user_sets(self, user_id: str) -> Iterable[SetORM]:
        pass
