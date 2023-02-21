from typing import NamedTuple, Iterable


class SetStat(NamedTuple):
    count: int
    count_to_repeat: int
    count_finished: int


class SetInfo(NamedTuple):
    name: str
    is_mutable: bool
    stat: SetStat


class PageOfCards(NamedTuple):
    terms: Iterable[str]
    page: int
    max_page: int
