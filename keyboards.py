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


def get_main_menu(language: str) -> Tuple[str, ...]:
    return (
        CHANGE_LANGUAGE[language],
        LOOK_SET_INFO[language],
        LEARN_SET[language],
        ADD_SET[language],
        DELETE_SET[language],
    )


def get_back(language: str) -> Tuple[str, ...]:
    return (
        BACK[language],
    )


def get_back_or_without_sample(language: str) -> Tuple[str, ...]:
    return (
        WITHOUT_SAMPLE[language],
        BACK[language],
    )


def get_cancel(language: str) -> Tuple[str, ...]:
    return (
        CANCEL[language],
    )


def get_ui_languages(language: str) -> Tuple[str, ...]:
    return (
        ENGLISH_LANGUAGE[language],
        RUSSIAN_LANGUAGE[language],
    )


def get_sets(sets_names: Iterable[str], language: str) -> List[str]:
    keyboard = [set_name for set_name in sets_names]
    keyboard.append(BACK[language])
    return keyboard


def get_add_set_menu(language: str) -> Tuple[str, ...]:
    return (
        NEW_SET[language],
        EXIST_SET[language],
        BACK[language],
    )


def get_mutable_set_info_menu(language: str) -> Tuple[str, ...]:
    return (
        SHOW_ALL_CARDS[language],
        ADD_CARD[language],
        DELETE_CARD[language],
        LEARN[language],
        BACK[language],
    )


def get_immutable_set_info_menu(language: str) -> Tuple[str, ...]:
    return (
        SHOW_ALL_CARDS[language],
        LEARN[language],
        BACK[language],
    )


def get_look_set_info(language: str) -> Tuple[str, ...]:
    return (
        LOOK_SET_INFO[language],
    )
