from typing import NamedTuple


class SetStat(NamedTuple):
    count: int
    count_to_repeat: int
    count_finished: int


class SetInfo(NamedTuple):
    name: str
    is_mutable: bool
    stat: SetStat
