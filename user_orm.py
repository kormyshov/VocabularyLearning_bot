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


class UserORM(NamedTuple):
    id: str
    state: UserState
    data: int
