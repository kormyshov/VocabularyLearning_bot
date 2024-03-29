import os
import ydb
import random
from datetime import date
from typing import Collection, Iterable

from card_info import CardInfo
from logging_decorator import logger
from set_orm import SetORM
from set_info import SetStat
from user_orm import UserORM
from repetition_orm import RepetitionORM
from sm import SM
from abstract_base import (
    AbstractBase,
    UserDoesntExistInDB,
    SetDoesntExistInDB,
    TermDoesntExistInDB,
    DefinitionDoesntExistInDB,
    SampleDoesntExistInDB,
    CardDoesntExistInDB,
    SetIsEmpty,
    RepetitionDoesntExistInDB,
    AllTermsRepeated,
)


class Database(AbstractBase):

    @logger
    def __init__(self):
        self.driver = ydb.Driver(
            endpoint=os.getenv('YDB_ENDPOINT'),
            database=os.getenv('YDB_DATABASE'),
            credentials=ydb.construct_credentials_from_environ(),
        )
        self.driver.wait(fail_fast=True, timeout=5)
        self.pool = ydb.SessionPool(self.driver)

    def __del__(self):
        self.pool.stop()
        self.driver.stop()

    @logger
    def get_user_info(self, user_id: str) -> UserORM:
        def select(session):
            return session.transaction().execute(
                'SELECT `id`, `state`, `set_id`, `term_id`, `definition_id`, `sample_id`, `card_id`, `language` FROM `users` WHERE `id` == "{}";'.format(user_id),
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
            language=result[0].rows[0].language.decode('utf-8'),
        )

    @logger
    def set_user_info(self, user: UserORM) -> None:
        def upsert(session):
            return session.transaction().execute(
                'UPSERT INTO `users` (`id`, `state`, `set_id`, `term_id`, `definition_id`, `sample_id`, `card_id`, `language`) VALUES ("{}", {}, {}, {}, {}, {}, {}, "{}");'.format(
                    user.id,
                    user.state,
                    user.set_id,
                    user.term_id,
                    user.definition_id,
                    user.sample_id,
                    user.card_id,
                    user.language,
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
    def set_user_language(self, user_id: str, language: str) -> None:
        def upsert(session):
            return session.transaction().execute(
                'UPSERT INTO `users` (`id`, `language`) VALUES ("{}", "{}");'.format(
                    user_id,
                    language,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        self.pool.retry_operation_sync(upsert)

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

        while True:
            set_id = int(user_id) * 1000 + random.randint(0, 999)

            def select(session):
                return session.transaction().execute(
                    'SELECT `id` FROM `sets` WHERE `id` == {};'.format(set_id),
                    commit_tx=True,
                    settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
                )

            result = self.pool.retry_operation_sync(select)

            if len(result[0].rows) == 0:
                break

        def upsert(session):
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
                '''
                    SELECT COUNT(*) as `count` FROM `cards` as `a`
                    JOIN (
                        SELECT `origin_set_id` as `set_id` FROM `sets` WHERE `id` == {}
                    ) as `b`
                    USING(`set_id`)
                    ;
                '''.format(
                    set_id,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)

        return result[0].rows[0].count

    @logger
    def get_set_stat(self, user_id: str, set_id: int, repetition_interval_to_finished: int) -> SetStat:
        def select(session):
            return session.transaction().execute(
                '''
                    SELECT
                        COUNT(*) as `count`,
                        COUNT_IF(
                            `last_repetition` IS NULL OR 
                            CAST(`last_repetition` as Date) + DateTime::IntervalFromDays(CAST(`repetition_interval` ?? 0 as Int32)) <= CurrentUtcDate()
                        ) as `count_to_repeat`,
                        COUNT_IF(
                            CAST(`repetition_interval` ?? 0 as Int32) > {}
                        ) as `count_finished`,
                        AVG(`repetition_interval` ?? 0) ?? 0 as `mean_repetition`,
                    FROM (
                        SELECT `id` FROM `cards` as `a`
                        JOIN (
                            SELECT `origin_set_id` as `set_id` FROM `sets` WHERE `id` == {}
                        ) as `b`
                        USING(`set_id`)
                    ) as `a`
                    LEFT JOIN (
                        SELECT `card_id`, `repetition_interval`, `last_repetition` FROM `repeats` WHERE `user_id` == "{}"
                    ) as `b`
                    ON `a`.`id` == `b`.`card_id`
                    ;
                '''.format(
                    repetition_interval_to_finished,
                    set_id,
                    user_id,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)

        return SetStat(
            result[0].rows[0].count,
            result[0].rows[0].count_to_repeat,
            result[0].rows[0].count_finished,
            result[0].rows[0].mean_repetition,
        )

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

        while True:
            term_id = set_id * 1000000 + random.randint(0, 999999)

            def select(session):
                return session.transaction().execute(
                    'SELECT `id` FROM `terms` WHERE `id` == {};'.format(term_id),
                    commit_tx=True,
                    settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
                )

            result = self.pool.retry_operation_sync(select)

            if len(result[0].rows) == 0:
                break

        def upsert(session):
            return session.transaction().execute(
                'UPSERT INTO `terms` (`id`, `term`) VALUES ({}, "{}");'.format(term_id, term),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        self.pool.retry_operation_sync(upsert)

        return term_id

    @logger
    def get_definition_id(self, term_id: int, definition: str) -> int:
        def select(session):
            return session.transaction().execute(
                'SELECT `id` FROM `definitions` WHERE `definition` == "{}" AND `term_id` == {};'.format(
                    definition,
                    term_id,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)

        if len(result[0].rows) == 0:
            raise DefinitionDoesntExistInDB

        return result[0].rows[0].id

    @logger
    def create_definition(self, set_id: int, term_id: int, definition: str) -> int:

        while True:
            definition_id = set_id * 1000000 + random.randint(0, 999999)

            def select(session):
                return session.transaction().execute(
                    'SELECT `id` FROM `definitions` WHERE `id` == {};'.format(definition_id),
                    commit_tx=True,
                    settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
                )

            result = self.pool.retry_operation_sync(select)

            if len(result[0].rows) == 0:
                break

        def upsert(session):
            return session.transaction().execute(
                'UPSERT INTO `definitions` (`id`, `term_id`, `definition`) VALUES ({}, {}, "{}");'.format(
                    definition_id,
                    term_id,
                    definition,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        self.pool.retry_operation_sync(upsert)

        return definition_id

    @logger
    def get_sample_id(self, term_id: int, sample: str) -> int:
        def select(session):
            return session.transaction().execute(
                'SELECT `id` FROM `samples` WHERE `sample` == "{}" AND `term_id` == {};'.format(
                    sample,
                    term_id,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)

        if len(result[0].rows) == 0:
            raise SampleDoesntExistInDB

        return result[0].rows[0].id

    @logger
    def create_sample(self, set_id: int, term_id: int, sample: str) -> int:

        while True:
            sample_id = set_id * 1000000 + random.randint(0, 999999)

            def select(session):
                return session.transaction().execute(
                    'SELECT `id` FROM `samples` WHERE `id` == {};'.format(sample_id),
                    commit_tx=True,
                    settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
                )

            result = self.pool.retry_operation_sync(select)

            if len(result[0].rows) == 0:
                break

        def upsert(session):
            return session.transaction().execute(
                'UPSERT INTO `samples` (`id`, `term_id`, `sample`) VALUES ({}, {}, "{}");'.format(
                    sample_id,
                    term_id,
                    sample,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        self.pool.retry_operation_sync(upsert)

        return sample_id

    @logger
    def create_card(self, set_id: int, term_id: int, definition_id: int, sample_id: int) -> int:

        while True:
            card_id = set_id * 1000000 + random.randint(0, 999999)

            def select(session):
                return session.transaction().execute(
                    'SELECT `id` FROM `cards` WHERE `id` == {};'.format(card_id),
                    commit_tx=True,
                    settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
                )

            result = self.pool.retry_operation_sync(select)

            if len(result[0].rows) == 0:
                break

        def upsert(session):
            return session.transaction().execute(
                'UPSERT INTO `cards` (`id`, `set_id`, `term_id`, `definition_id`, `sample_id`) VALUES ({}, {}, {}, {}, {});'.format(
                    card_id,
                    set_id,
                    term_id,
                    definition_id,
                    sample_id,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        self.pool.retry_operation_sync(upsert)

        return card_id

    @logger
    def get_card_info(self, card_id: int) -> CardInfo:
        def select(session):
            return session.transaction().execute(
                '''
                    SELECT
                        `term`, `definition`, `sample`
                    FROM (
                        SELECT `term_id`, `definition_id`, `sample_id` FROM `cards` WHERE `id` == {}
                    ) as `a`
                    LEFT JOIN `terms` as `b`
                    ON `a`.`term_id` == `b`.`id`
                    LEFT JOIN `definitions` as `c`
                    ON `a`.`definition_id` == `c`.`id`
                    LEFT JOIN `samples` as `d`
                    ON `a`.`sample_id` == `d`.`id`
                    ;
                '''.format(
                    card_id,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)

        if len(result[0].rows) == 0:
            raise CardDoesntExistInDB

        return CardInfo(
            term=result[0].rows[0].term.decode('utf-8'),
            definition=result[0].rows[0].definition.decode('utf-8'),
            sample=result[0].rows[0].sample.decode('utf-8'),
        )

    @logger
    def get_terms_of_set(self, set_id: int, limit: int, offset: int) -> Iterable[str]:
        def select(session):
            return session.transaction().execute(
                '''
                    SELECT
                        `term`
                    FROM (
                        SELECT `term_id` FROM `cards` as `a`
                        JOIN (
                            SELECT `origin_set_id` as `set_id` FROM `sets` WHERE `id` == {}
                        ) as `b`
                        USING(`set_id`)
                    ) as `a`
                    LEFT JOIN `terms` as `b`
                    ON `a`.`term_id` == `b`.`id`
                    ORDER BY `term`
                    LIMIT {} OFFSET {}
                    ;
                '''.format(
                    set_id,
                    limit,
                    offset,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)

        return map(lambda row: row.term.decode('utf-8'), result[0].rows)

    @logger
    def get_card_of_set_by_term(self, set_id: int, term: str) -> int:
        def select(session):
            return session.transaction().execute(
                '''
                    SELECT
                        `b`.`id` as `id`
                    FROM (
                        SELECT `id` FROM `terms` WHERE `term` == "{}"
                    ) as `a`
                    LEFT JOIN (
                        SELECT `id`, `term_id` FROM `cards` as `a`
                        JOIN (
                            SELECT `origin_set_id` as `set_id` FROM `sets` WHERE `id` == {}
                        ) as `b`
                        USING(`set_id`)
                    ) as `b`
                    ON `a`.`id` == `b`.`term_id`
                    ;
                '''.format(
                    term,
                    set_id,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)

        if len(result[0].rows) == 0:
            raise CardDoesntExistInDB

        return result[0].rows[0].id

    @logger
    def delete_card_by_id(self, card_id) -> None:
        def upsert(session):
            return session.transaction().execute(
                'UPSERT INTO `cards` (`id`, `set_id`, `term_id`, `definition_id`, `sample_id`) VALUES ({}, 0, 0, 0, 0)'.format(card_id),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        self.pool.retry_operation_sync(upsert)

    @logger
    def get_card_id_to_repeat(self, user_id: str, set_id: int) -> int:
        def select(session):
            return session.transaction().execute(
                '''
                    SELECT
                        `a`.`id` as `id`,
                        IF (`last_repetition` IS NULL,
                            "1970-01-01",
                            CAST(CAST(`last_repetition` as Date) + DateTime::IntervalFromDays(CAST(`repetition_interval` ?? 0 as Int32)) as String)
                        ) as `next_repetition`,
                    FROM (
                        SELECT `id` FROM `cards` as `a`
                        JOIN (
                            SELECT `origin_set_id` as `set_id` FROM `sets` WHERE `id` == {}
                        ) as `b`
                        USING(`set_id`)
                    ) as `a`
                    LEFT JOIN (
                        SELECT `card_id`, `repetition_interval`, `last_repetition` FROM `repeats` WHERE `user_id` == "{}"
                    ) as `b`
                    ON `a`.`id` == `b`.`card_id`
                    ORDER BY `next_repetition`
                    LIMIT 1
                    ;
                '''.format(
                    set_id,
                    user_id,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)

        if len(result[0].rows) == 0:
            raise SetIsEmpty

        if result[0].rows[0].next_repetition.decode('utf-8') > str(date.today()):
            raise AllTermsRepeated

        return result[0].rows[0].id

    @logger
    def get_repetition(self, user_id: str, card_id: int) -> RepetitionORM:
        def select(session):
            return session.transaction().execute(
                '''
                    SELECT
                        `user_id`,
                        `card_id`,
                        `repetition_number`,
                        `easiness_factor`,
                        `repetition_interval`,
                        `last_repetition`
                    FROM `repeats`
                    WHERE `user_id` == "{}" AND `card_id` == {}
                    ;
                '''.format(
                    user_id,
                    card_id,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        result = self.pool.retry_operation_sync(select)

        if len(result[0].rows) == 0:
            raise RepetitionDoesntExistInDB

        return RepetitionORM(
            user_id=result[0].rows[0].user_id,
            card_id=result[0].rows[0].card_id,
            sm=SM(
                repetition_number=result[0].rows[0].repetition_number,
                easiness_factor=result[0].rows[0].easiness_factor,
                repetition_interval=result[0].rows[0].repetition_interval,
            ),
            last_repetition=result[0].rows[0].last_repetition,
        )

    @logger
    def set_repetition(self, repetition: RepetitionORM) -> None:
        def upsert(session):
            return session.transaction().execute(
                '''
                    UPSERT INTO `repeats` (
                        `user_id`,
                        `card_id`,
                        `repetition_number`,
                        `easiness_factor`,
                        `repetition_interval`,
                        `last_repetition`
                    ) VALUES (
                        "{}", {}, {}, {}, {}, "{}"
                    )
                    ;
                '''.format(
                    repetition.user_id,
                    repetition.card_id,
                    repetition.sm.repetition_number,
                    repetition.sm.easiness_factor,
                    repetition.sm.repetition_interval,
                    repetition.last_repetition,
                ),
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
            )

        self.pool.retry_operation_sync(upsert)
