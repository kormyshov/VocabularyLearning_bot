from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import BACK, THERE_IS_NO_SET, LOOK_SET_INFO, CANCEL, SET_STAT
from set_info import SetInfo
from keyboards import get_mutable_set_info_menu, get_immutable_set_info_menu
from controller.utils import parse_set_id_from_button_name, validate_set_id_in_button_name


class LookSetInfoAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return (
            (user.is_request_to_look_set_info() and text != BACK[user.language]) or
            (user.is_request_to_add_term() and text == BACK[user.language]) or
            (user.is_look_card_info() and text == LOOK_SET_INFO[user.language]) or
            (user.is_request_to_delete_card() and text == BACK[user.language]) or
            (user.is_request_term_by_definition() and text == CANCEL[user.language]) or
            (user.is_request_term_by_sample() and text == CANCEL[user.language]) or
            (user.is_request_term_by_mask() and text == CANCEL[user.language])
        )

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        info: SetInfo = user.look_set_info(
            parse_set_id_from_button_name(text) if validate_set_id_in_button_name(text) else user.set_id
        )
        if info is not None:
            viewer.view(
                user.id,
                '<b>{}</b>\n\n{}'.format(
                    info.name,
                    SET_STAT[user.language].format(info.stat.count, info.stat.count_to_repeat, info.stat.count_finished),
                ),
                get_mutable_set_info_menu(user.language) if info.is_mutable else get_immutable_set_info_menu(user.language)
            )
        else:
            viewer.view(user.id, THERE_IS_NO_SET[user.language])
