from typing import Tuple, Iterable, List
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


def get_sets(sets_names: Iterable[str]) -> List[str]:
    keyboard = [set_name for set_name in sets_names]
    keyboard.append(constants.BACK)
    return keyboard


def get_add_set_menu() -> Tuple[str, ...]:
    return (
        constants.NEW_SET,
        constants.EXIST_SET,
        constants.BACK,
    )
