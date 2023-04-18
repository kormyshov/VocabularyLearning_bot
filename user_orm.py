from typing import NamedTuple
from enum import IntEnum


class UserState(IntEnum):
    START = 0
    REQUEST_TO_LOOK_SET_INFO = 1
    LOOK_SET_INFO = 2
    REQUEST_TO_ADD_SET = 3
    REQUEST_TO_ADD_EXIST_SET = 4
    REQUEST_TO_ADD_NEW_SET = 5
    REQUEST_TO_DELETE_SET = 6
    REQUEST_TO_ADD_TERM = 7
    REQUEST_TO_ADD_DEFINITION = 8
    REQUEST_TO_ADD_SAMPLE = 9
    LOOK_CARD_INFO = 10
    REQUEST_TO_LEARN_SET = 11
    REQUEST_TO_DELETE_CARD = 12
    REQUEST_TERM_BY_DEFINITION = 13
    REQUEST_TERM_BY_SAMPLE = 14
    REQUEST_TERM_BY_MASK = 15
    REQUEST_TO_CHANGE_LANGUAGE = 16


class UserORM(NamedTuple):
    id: str
    state: UserState
    set_id: int
    term_id: int
    definition_id: int
    sample_id: int
    card_id: int
    language: str
