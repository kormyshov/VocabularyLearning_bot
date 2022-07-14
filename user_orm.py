from typing import NamedTuple
from enum import IntEnum


class UserState(IntEnum):
    START = 0
    LOOK_SET_INFO = 1


class UserORM(NamedTuple):
    id: str
    state: UserState
    data: int
