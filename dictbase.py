from typing import Collection
from abstract_base import AbstractBase, UserDoesntExistInDB, SetDoesntExistInDB
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

    def get_user_sets(self, user_id: str) -> Collection[SetORM]:
        return self.sets.get(user_id, [])

    def get_set_by_id(self, set_id: int) -> SetORM:
        if set_id not in self.sets:
            raise SetDoesntExistInDB
        return self.sets[set_id]

    def copy_set(self, user_id: str, set_name: str, set_id: int) -> None:
        pass
