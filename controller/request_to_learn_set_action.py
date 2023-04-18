from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import LEARN_SET, YOU_DONT_HAVE_SET, SELECT_SET
import keyboards


class RequestToLearnSetAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_main_menu() and text == LEARN_SET[user.language]

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        user_set_names = user.request_to_learn_set()
        keyboard = keyboards.get_sets(user_set_names, user.language)
        if len(keyboard) == 1:
            user.go_to_main_menu()
            viewer.view(user.id, YOU_DONT_HAVE_SET[user.language], keyboards.get_main_menu(user.language))
        else:
            viewer.view(user.id, SELECT_SET[user.language], keyboard)
