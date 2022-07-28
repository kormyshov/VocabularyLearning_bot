from typing import NamedTuple
from enum import IntEnum


class UserState(IntEnum):
    START = 0
    REQUEST_TO_LOOK_SET_INFO = 1
    LOOK_SET_INFO = 2
    REQUEST_TO_ADD_SET = 3


class UserORM(NamedTuple):
    id: str
    state: UserState
    data: int
