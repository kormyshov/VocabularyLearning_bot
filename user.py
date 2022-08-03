from typing import Iterable, Collection
from logging_decorator import logger
from abstract_base import AbstractBase, UserDoesntExistInDB, SetDoesntExistInDB
from user_orm import UserState, UserORM
from set_orm import SetORM


MAX_SET_COUNT = 5


class User:
    def __init__(self, chat_id: str, database: AbstractBase) -> None:
        self.id: str = chat_id
        self.database: AbstractBase = database
        self.loaded: bool = False
        self.state: UserState = UserState.START
        self.data: int = 0

    def __str__(self) -> str:
        return 'User(id: {}, state: {})'.format(
            self.id,
            str(self.state),
        )

    @logger
    def load(self) -> None:
        if not self.loaded:
            try:
                response: UserORM = self.database.get_user_info(self.id)
                self.state = response.state
                self.data = response.data
            except UserDoesntExistInDB:
                pass

            self.loaded = True

    @logger
    def save(self) -> None:
        self.database.set_user_info(UserORM(
            id=self.id,
            state=self.state,
            data=self.data,
        ))

    @logger
    def get_sets(self) -> Collection[SetORM]:
        return self.database.get_user_sets(self.id)

    @logger
    def request_to_look_set_info(self) -> Iterable[str]:
        self.state = UserState.REQUEST_TO_LOOK_SET_INFO
        return map(lambda e: '{}: {}'.format(e.id, e.name), self.get_sets())

    @logger
    def is_request_to_look_set_info(self) -> bool:
        return self.state == UserState.REQUEST_TO_LOOK_SET_INFO

    @logger
    def request_to_add_set(self) -> bool:
        if len(self.get_sets()) >= MAX_SET_COUNT:
            return False
        self.state = UserState.REQUEST_TO_ADD_SET
        return True

    @logger
    def is_request_to_add_set(self) -> bool:
        return self.state == UserState.REQUEST_TO_ADD_SET

    @logger
    def request_to_add_exist_set(self) -> None:
        self.state = UserState.REQUEST_TO_ADD_EXIST_SET

    @logger
    def is_request_to_add_exist_set(self) -> bool:
        return self.state == UserState.REQUEST_TO_ADD_EXIST_SET

    @logger
    def request_to_add_new_set(self) -> None:
        self.state = UserState.REQUEST_TO_ADD_NEW_SET

    @logger
    def is_request_to_add_new_set(self) -> bool:
        return self.state == UserState.REQUEST_TO_ADD_NEW_SET

    @logger
    def add_exist_set(self, set_id: int) -> bool:
        try:
            set_orm = self.database.get_set_by_id(set_id)
            self.database.copy_set(self.id, set_orm.name, set_orm.origin_set_id)
            return True
        except SetDoesntExistInDB:
            return False

    @logger
    def add_new_set(self, set_name: str) -> None:
        self.database.create_set(self.id, set_name)

    @logger
    def go_to_main_menu(self) -> None:
        self.state = UserState.START

    @logger
    def is_main_menu(self) -> bool:
        return self.state == UserState.START
