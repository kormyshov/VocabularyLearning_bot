from logging_decorator import logger
from abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import BACK
from go_to_main_menu_action import GoToMainMenuAction


class LookSetInfoAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_request_to_look_set_info() and text != BACK

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        GoToMainMenuAction().do(viewer, user, text)
        pass
