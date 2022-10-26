from logging_decorator import logger
from abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import LOOK_SETS, YOU_DONT_HAVE_SET


class LookSetsAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_main_menu() and text == LOOK_SETS

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        is_empty = True
        for user_set in user.get_sets():
            viewer.view(user.id, '{}. {}'.format(user_set.id, user_set.name))
            is_empty = False
        if is_empty:
            viewer.view(user.id, YOU_DONT_HAVE_SET)
