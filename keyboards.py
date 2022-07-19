from typing import Tuple
import constants


def get_main_menu() -> Tuple[str, ...]:
    return (
        constants.LOOK_SETS,
        constants.LOOK_SET_INFO,
        constants.LEARN_SET,
        constants.ADD_SET,
        constants.DELETE_SET,
    )


def get_back() -> Tuple[str, ...]:
    return (
        constants.BACK,
    )
