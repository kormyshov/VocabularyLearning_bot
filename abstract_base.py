from abc import ABC, abstractmethod
from typing import Iterable
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
    def get_user_sets(self, user_id: str) -> Iterable[SetORM]:
        pass


class UserDoesntExistInDB(Exception):
    pass
