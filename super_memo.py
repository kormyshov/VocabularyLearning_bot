from typing import Union, Literal
from sm import SM


Grade = Union[Literal[0], Literal[1], Literal[2], Literal[3], Literal[4], Literal[5]]


def change_sm(old: SM, grade: Grade) -> SM:
    repetition_number = old.repetition_number
    easiness_factor = old.easiness_factor
    repetition_interval = old.repetition_interval
    if grade >= 3:
        if repetition_number == 0:
            repetition_interval = 1
        elif repetition_number == 1:
            repetition_interval = 6
        else:
            repetition_interval = int(repetition_interval * easiness_factor)
        repetition_number += 1
    else:
        repetition_number = 0
        repetition_interval = 1

    easiness_factor += 0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02)
    easiness_factor = max(1.3, easiness_factor)

    return SM(repetition_number, easiness_factor, repetition_interval)
