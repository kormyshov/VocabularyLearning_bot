from typing import Tuple, Iterable, List
from constants import (
    CHANGE_LANGUAGE,
    LOOK_SET_INFO,
    LEARN_SET,
    ADD_SET,
    DELETE_SET,
    BACK,
    WITHOUT_SAMPLE,
    CANCEL,
    ENGLISH_LANGUAGE,
    RUSSIAN_LANGUAGE,
    NEW_SET,
    EXIST_SET,
    SHOW_ALL_CARDS,
    ADD_CARD,
    DELETE_CARD,
    LEARN,
)


def get_main_menu() -> Tuple[str, ...]:
    return (
        CHANGE_LANGUAGE['en'],
        LOOK_SET_INFO['en'],
        LEARN_SET['en'],
        ADD_SET['en'],
        DELETE_SET['en'],
    )


def get_back() -> Tuple[str, ...]:
    return (
        BACK['en'],
    )


def get_back_or_without_sample() -> Tuple[str, ...]:
    return (
        WITHOUT_SAMPLE['en'],
        BACK['en'],
    )


def get_cancel() -> Tuple[str, ...]:
    return (
        CANCEL['en'],
    )


def get_ui_languages() -> Tuple[str, ...]:
    return (
        ENGLISH_LANGUAGE['en'],
        RUSSIAN_LANGUAGE['en'],
    )


def get_sets(sets_names: Iterable[str]) -> List[str]:
    keyboard = [set_name for set_name in sets_names]
    keyboard.append(BACK['en'])
    return keyboard


def get_add_set_menu() -> Tuple[str, ...]:
    return (
        NEW_SET['en'],
        EXIST_SET['en'],
        BACK['en'],
    )


def get_mutable_set_info_menu() -> Tuple[str, ...]:
    return (
        SHOW_ALL_CARDS['en'],
        ADD_CARD['en'],
        DELETE_CARD['en'],
        LEARN['en'],
        BACK['en'],
    )


def get_immutable_set_info_menu() -> Tuple[str, ...]:
    return (
        SHOW_ALL_CARDS['en'],
        LEARN['en'],
        BACK['en'],
    )


def get_look_set_info() -> Tuple[str, ...]:
    return (
        LOOK_SET_INFO['en'],
    )
