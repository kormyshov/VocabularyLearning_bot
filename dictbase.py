from typing import Iterable
from abstract_base import AbstractBase, UserDoesntExistInDB
from set_orm import SetORM
from user_orm import UserORM


class Dictbase(AbstractBase):
    def __init__(self) -> None:
        self.users = dict()
        self.sets = dict()

    def __str__(self) -> str:
        return 'users: {}, sets: {}'.format(str(self.users), str(self.sets))

    def get_user_info(self, user_id: str) -> UserORM:
        if user_id not in self.users:
            raise UserDoesntExistInDB
        return self.users[user_id]

    def set_user_info(self, user: UserORM) -> None:
        self.users[user.id] = user

    def get_user_sets(self, user_id: str) -> Iterable[SetORM]:
        return self.sets.get(user_id, [])
