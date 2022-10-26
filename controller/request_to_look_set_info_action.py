from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import LOOK_SET_INFO, YOU_DONT_HAVE_SET, SELECT_SET
import keyboards


class RequestToLookSetInfoAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_main_menu() and text == LOOK_SET_INFO

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        user_set_names = user.request_to_look_set_info()
        keyboard = keyboards.get_sets(user_set_names)
        if len(keyboard) == 1:
            user.go_to_main_menu()
            viewer.view(user.id, YOU_DONT_HAVE_SET, keyboards.get_main_menu())
        else:
            viewer.view(user.id, SELECT_SET, keyboard)
