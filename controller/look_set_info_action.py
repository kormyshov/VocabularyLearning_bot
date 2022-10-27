from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import BACK, THERE_IS_NO_SET
from set_info import SetInfo
from keyboards import get_mutable_set_info_menu, get_immutable_set_info_menu


class LookSetInfoAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_request_to_look_set_info() and text != BACK

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        info: SetInfo = user.look_set_info(int(text.split(':')[0]))
        if info is not None:
            viewer.view(
                user.id,
                '**{}**\n\n{} cards'.format(info.name, info.count_of_cards),
                get_mutable_set_info_menu() if info.is_mutable else get_immutable_set_info_menu()
            )
        else:
            viewer.view(user.id, THERE_IS_NO_SET)
