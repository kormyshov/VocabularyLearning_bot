from typing import Tuple, Iterable, List
import constants


def get_main_menu() -> Tuple[str, ...]:
    return (
        constants.CHANGE_LANGUAGE,
        constants.LOOK_SET_INFO,
        constants.LEARN_SET,
        constants.ADD_SET,
        constants.DELETE_SET,
    )


def get_back() -> Tuple[str, ...]:
    return (
        constants.BACK,
    )


def get_back_or_without_sample() -> Tuple[str, ...]:
    return (
        constants.WITHOUT_SAMPLE,
        constants.BACK,
    )


def get_cancel() -> Tuple[str, ...]:
    return (
        constants.CANCEL,
    )


def get_ui_languages() -> Tuple[str, ...]:
    return (
        constants.ENGLISH_LANGUAGE,
        constants.RUSSIAN_LANGUAGE,
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


def get_mutable_set_info_menu() -> Tuple[str, ...]:
    return (
        constants.SHOW_ALL_CARDS,
        constants.ADD_CARD,
        constants.DELETE_CARD,
        constants.LEARN,
        constants.BACK,
    )


def get_immutable_set_info_menu() -> Tuple[str, ...]:
    return (
        constants.SHOW_ALL_CARDS,
        constants.LEARN,
        constants.BACK,
    )


def get_look_set_info() -> Tuple[str, ...]:
    return (
        constants.LOOK_SET_INFO,
    )
