from logging_decorator import logger
from abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import BACK, SET_HAS_BEEN_CREATED
from go_to_main_menu_action import GoToMainMenuAction


class AddNewSetAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_request_to_add_new_set() and text != BACK

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        user.add_new_set(text)
        viewer.view(user.id, SET_HAS_BEEN_CREATED)
        GoToMainMenuAction().do(viewer, user, text)
