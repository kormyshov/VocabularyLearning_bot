from abc import ABC, abstractmethod
from typing import Collection
from set_orm import SetORM
from user_orm import UserORM
from card_info import CardInfo


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
    def get_user_set_by_id(self, user_id: str, set_id: int) -> SetORM:
        pass

    @abstractmethod
    def copy_set(self, user_id: str, set_name: str, set_id: int) -> None:
        pass

    @abstractmethod
    def create_set(self, user_id: str, set_name: str) -> None:
        pass

    @abstractmethod
    def disconnect_set_and_user(self, set_id: int) -> None:
        pass

    @abstractmethod
    def get_count_of_cards(self, set_id: int) -> int:
        pass

    @abstractmethod
    def get_term_id(self, term: str) -> int:
        pass

    @abstractmethod
    def create_term(self, set_id: int, term: str) -> int:
        pass

    @abstractmethod
    def get_definition_id(self, term_id: int, definition: str) -> int:
        pass

    @abstractmethod
    def create_definition(self, set_id: int, term_id: int, definition: str) -> int:
        pass

    @abstractmethod
    def get_sample_id(self, term_id: int, sample: str) -> int:
        pass

    @abstractmethod
    def create_sample(self, set_id: int, term_id: int, sample: str) -> int:
        pass

    @abstractmethod
    def create_card(self, set_id: int, term_id: int, definition_id: int, sample_id: int) -> int:
        pass

    @abstractmethod
    def get_card_info(self, card_id: int) -> CardInfo:
        pass


class UserDoesntExistInDB(Exception):
    pass


class SetDoesntExistInDB(Exception):
    pass


class TermDoesntExistInDB(Exception):
    pass


class DefinitionDoesntExistInDB(Exception):
    pass


class SampleDoesntExistInDB(Exception):
    pass


class CardDoesntExistInDB(Exception):
    pass
