from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from controller.go_to_main_menu_action import GoToMainMenuAction


class ChangeLanguageAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_request_to_change_language()

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        user.change_language(text)
        GoToMainMenuAction().do(viewer, user, text)
