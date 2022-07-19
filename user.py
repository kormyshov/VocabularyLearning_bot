from typing import Iterable
from logging_decorator import logger
from abstract_base import AbstractBase, UserDoesntExistInDB
from user_orm import UserState, UserORM
from set_orm import SetORM


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
    def get_sets(self) -> Iterable[SetORM]:
        return self.database.get_user_sets(self.id)
