from abc import ABC, abstractmethod
from typing import Collection
from set_orm import SetORM
from user_orm import UserORM


class AbstractBase(ABC):
    @abstractmethod
    def get_user_info(self, user_id: str) -> UserORM:
        pass

    @abstractmethod
    def set_user_info(self, user: UserORM) -> None:
        pass

    @abstractmethod
    def get_user_sets(self, user_id: str) -> Collection[SetORM]:
        pass

    @abstractmethod
    def get_set_by_id(self, set_id: int) -> SetORM:
        pass

    @abstractmethod
    def copy_set(self, user_id: str, set_name: str, set_id: int) -> None:
        pass


class UserDoesntExistInDB(Exception):
    pass


class SetDoesntExistInDB(Exception):
    pass
