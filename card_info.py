from typing import NamedTuple, Optional


class CardInfo(NamedTuple):
    term: str
    definition: str
    sample: Optional[str]
