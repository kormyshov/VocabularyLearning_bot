from typing import Iterable, Collection, Optional
from logging_decorator import logger
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
from user_orm import UserState, UserORM
from set_orm import SetORM
from set_info import SetInfo, PageOfCards
from card_info import CardInfo
from repetition_orm import RepetitionORM
from super_memo import Grade, change_sm
from sm import get_default_sm
from datetime import date
from constants import WITHOUT_SAMPLE, ENGLISH_LANGUAGE, RUSSIAN_LANGUAGE


MAX_SET_COUNT = 5
MAX_CARD_COUNT = 1000
TERMS_ON_PAGE = 50


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
    def request_to_change_language(self) -> None:
        self.state = UserState.REQUEST_TO_CHANGE_LANGUAGE

    @logger
    def is_request_to_change_language(self) -> bool:
        return self.state == UserState.REQUEST_TO_CHANGE_LANGUAGE

    @logger
    def change_language(self, language_name: str) -> None:
        map_name_to_abbr = {
            ENGLISH_LANGUAGE['en']: 'en',
            RUSSIAN_LANGUAGE['en']: 'ru',
        }
        self.database.set_user_language(self.id, map_name_to_abbr[language_name])

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
            set_stat = self.database.get_set_stat(self.id, set_id)
            self.state = UserState.LOOK_SET_INFO
            self.set_id = set_orm.id
            return SetInfo(set_orm.name, set_orm.id == set_orm.origin_set_id, set_stat)
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

    @logger
    def add_sample(self, sample: str) -> int:
        try:
            sample_id = self.database.get_sample_id(self.term_id, sample)
        except SampleDoesntExistInDB:
            sample_id = self.database.create_sample(self.set_id, self.term_id, sample)
        return sample_id

    @logger
    def add_card(self, set_id: int, term_id: int, definition_id: int, sample_id: int) -> int:
        return self.database.create_card(set_id, term_id, definition_id, sample_id)

    @logger
    def get_card_info(self, card_id: int) -> Optional[CardInfo]:
        try:
            card_info = self.database.get_card_info(card_id)
            if card_info.sample == WITHOUT_SAMPLE['en']:
                card_info = CardInfo(card_info.term, card_info.definition, None)
            return card_info
        except CardDoesntExistInDB:
            return None

    @logger
    def look_card_info(self, card_id: int) -> Optional[CardInfo]:
        card_info = self.get_card_info(card_id)
        self.state = UserState.LOOK_CARD_INFO
        self.card_id = card_id
        return card_info

    @logger
    def is_look_card_info(self) -> bool:
        return self.state == UserState.LOOK_CARD_INFO

    @logger
    def request_to_learn_set(self) -> Iterable[str]:
        self.state = UserState.REQUEST_TO_LEARN_SET
        return map(lambda e: '{}: {}'.format(e.id, e.name), self.get_sets())

    @logger
    def is_request_to_learn_set(self) -> bool:
        return self.state == UserState.REQUEST_TO_LEARN_SET

    @logger
    def request_to_delete_card(self) -> None:
        self.state = UserState.REQUEST_TO_DELETE_CARD

    @logger
    def is_request_to_delete_card(self) -> bool:
        return self.state == UserState.REQUEST_TO_DELETE_CARD

    @logger
    def delete_card(self, term: str) -> bool:
        try:
            card_id = self.database.get_card_of_set_by_term(self.set_id, term)
            self.database.delete_card_by_id(card_id)
            return True
        except CardDoesntExistInDB:
            return False

    @logger
    def request_term_by_definition(self, set_id: int) -> Optional[str]:
        try:
            card_id = self.database.get_card_id_to_repeat(self.id, set_id)
            self.state = UserState.REQUEST_TERM_BY_DEFINITION
            self.card_id = card_id
            return self.get_card_info(card_id).definition
        except SetIsEmpty:
            raise SetIsEmpty
        except AllTermsRepeated:
            raise AllTermsRepeated

    @logger
    def is_request_term_by_definition(self) -> bool:
        return self.state == UserState.REQUEST_TERM_BY_DEFINITION

    @logger
    def is_term_right(self, term: str) -> bool:
        card_info = self.get_card_info(self.card_id)
        return term.lower().strip() == card_info.term.lower().strip()

    @logger
    def get_sample_of_current_card(self) -> str:
        return self.get_card_info(self.card_id).sample

    @logger
    def request_term_by_sample(self) -> str:
        self.state = UserState.REQUEST_TERM_BY_SAMPLE
        return self.get_sample_of_current_card()

    @logger
    def is_request_term_by_sample(self) -> bool:
        return self.state == UserState.REQUEST_TERM_BY_SAMPLE

    @logger
    def update_repetition(self, grade: Grade) -> None:
        try:
            repetition_orm = self.database.get_repetition(self.id, self.card_id)
            sm = change_sm(repetition_orm.sm, grade)
        except RepetitionDoesntExistInDB:
            sm = get_default_sm()
        self.database.set_repetition(RepetitionORM(
            user_id=self.id,
            card_id=self.card_id,
            sm=sm,
            last_repetition=date.today().strftime('%Y-%m-%d'),
        ))

    @logger
    def get_term_of_current_card(self) -> str:
        return self.get_card_info(self.card_id).term

    @logger
    def request_term_by_mask(self) -> str:
        self.state = UserState.REQUEST_TERM_BY_MASK
        return self.get_term_of_current_card()

    @logger
    def is_request_term_by_mask(self) -> bool:
        return self.state == UserState.REQUEST_TERM_BY_MASK

    @logger
    def show_all_cards(self, page: int) -> PageOfCards:
        count_of_cards = self.database.get_count_of_cards(self.set_id)
        max_page = (count_of_cards + TERMS_ON_PAGE - 1) // TERMS_ON_PAGE
        terms = self.database.get_terms_of_set(self.set_id, TERMS_ON_PAGE, page * TERMS_ON_PAGE)
        return PageOfCards(
            terms=terms,
            page=page,
            max_page=max_page,
        )
