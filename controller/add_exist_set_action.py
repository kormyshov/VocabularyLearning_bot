from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import BACK, SET_HAS_BEEN_ADDED, THERE_IS_NO_SET
from controller.go_to_main_menu_action import GoToMainMenuAction


class AddExistSetAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_request_to_add_exist_set() and text != BACK[user.language]

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        if user.add_exist_set(int(text)):
            viewer.view(user.id, SET_HAS_BEEN_ADDED[user.language])
            GoToMainMenuAction().do(viewer, user, text)
        else:
            viewer.view(user.id, THERE_IS_NO_SET[user.language])
