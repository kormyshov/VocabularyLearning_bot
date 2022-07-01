from typing import NamedTuple


class SM(NamedTuple):
    repetition_number: int
    easiness_factor: float
    repetition_interval: int


def get_default_sm() -> SM:
    return SM(0, 2.5, 0)
