from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import BACK, MENU
import keyboards


class GoToMainMenuAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return (
            (user.is_request_to_add_set() and text == BACK) or
            (user.is_request_to_look_set_info() and text == BACK) or
            (user.is_request_to_delete_set() and text == BACK)
        )

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        user.go_to_main_menu()
        viewer.view(user.id, MENU, keyboards.get_main_menu())
