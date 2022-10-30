from typing import Iterable, Collection, Optional
from logging_decorator import logger
from abstract_base import (
    AbstractBase,
    UserDoesntExistInDB,
    SetDoesntExistInDB,
    TermDoesntExistInDB,
    DefinitionDoesntExistInDB,
)
from user_orm import UserState, UserORM
from set_orm import SetORM
from set_info import SetInfo


MAX_SET_COUNT = 5
MAX_CARD_COUNT = 1000


class User:
    def __init__(self, chat_id: str, database: AbstractBase) -> None:
        self.id: str = chat_id
        self.database: AbstractBase = database
        self.loaded: bool = False
        self.state: UserState = UserState.START
        self.set_id: int = 0
        self.term_id: int = 0
        self.definition_id: int = 0
        self.sample_id: int = 0
        self.card_id: int = 0

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
                self.set_id = response.set_id
                self.term_id = response.term_id
                self.definition_id = response.definition_id
                self.sample_id = response.sample_id
                self.card_id = response.card_id
            except UserDoesntExistInDB:
                pass

            self.loaded = True

    @logger
    def save(self) -> None:
        self.database.set_user_info(UserORM(
            id=self.id,
            state=self.state,
            set_id=self.set_id,
            term_id=self.term_id,
            definition_id=self.definition_id,
            sample_id=self.sample_id,
            card_id=self.card_id,
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
    def request_to_delete_set(self) -> Iterable[str]:
        self.state = UserState.REQUEST_TO_DELETE_SET
        return map(lambda e: '{}: {}'.format(e.id, e.name), self.get_sets())

    @logger
    def is_request_to_delete_set(self) -> bool:
        return self.state == UserState.REQUEST_TO_DELETE_SET

    @logger
    def delete_set(self, set_id: int) -> bool:
        try:
            self.database.get_user_set_by_id(self.id, set_id)
            self.database.disconnect_set_and_user(set_id)
            return True
        except SetDoesntExistInDB:
            return False

    @logger
    def go_to_main_menu(self) -> None:
        self.state = UserState.START

    @logger
    def is_main_menu(self) -> bool:
        return self.state == UserState.START

    @logger
    def look_set_info(self, set_id: int) -> Optional[SetInfo]:
        try:
            set_orm = self.database.get_user_set_by_id(self.id, set_id)
            count_of_cards = self.database.get_count_of_cards(set_orm.origin_set_id)
            self.state = UserState.LOOK_SET_INFO
            self.set_id = set_orm.origin_set_id
            return SetInfo(set_orm.name, count_of_cards, set_orm.id == set_orm.origin_set_id)
        except SetDoesntExistInDB:
            return None

    @logger
    def is_look_set_info(self) -> bool:
        return self.state == UserState.LOOK_SET_INFO

    @logger
    def request_to_add_term(self) -> bool:
        if self.database.get_count_of_cards(self.set_id) >= MAX_CARD_COUNT:
            return False
        self.state = UserState.REQUEST_TO_ADD_TERM
        return True

    @logger
    def is_request_to_add_term(self) -> bool:
        return self.state == UserState.REQUEST_TO_ADD_TERM

    @logger
    def request_to_add_definition(self, term_id: int) -> None:
        self.state = UserState.REQUEST_TO_ADD_DEFINITION
        self.term_id = term_id

    @logger
    def is_request_to_add_definition(self) -> bool:
        return self.state == UserState.REQUEST_TO_ADD_DEFINITION

    @logger
    def add_term(self, term: str) -> int:
        try:
            term_id = self.database.get_term_id(term)
        except TermDoesntExistInDB:
            term_id = self.database.create_term(self.set_id, term)
        return term_id

    @logger
    def request_to_add_sample(self, definition_id: int) -> None:
        self.state = UserState.REQUEST_TO_ADD_SAMPLE
        self.definition_id = definition_id

    @logger
    def is_request_to_add_sample(self) -> bool:
        return self.state == UserState.REQUEST_TO_ADD_SAMPLE

    @logger
    def add_definition(self, definition: str) -> int:
        try:
            definition_id = self.database.get_definition_id(self.term_id, definition)
        except DefinitionDoesntExistInDB:
            definition_id = self.database.create_definition(self.set_id, self.term_id, definition)
        return definition_id
