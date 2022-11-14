from typing import NamedTuple
from sm import SM


class RepetitionORM(NamedTuple):
    card_id: int
    user_id: str
    sm: SM
    last_repetition: str
