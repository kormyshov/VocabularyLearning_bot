import re
import random
from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import CANCEL, RIGHT, ENTER_TERM_WITH_MASK
import keyboards
from controller.request_term_by_definition_action import RequestTermByDefinitionAction


def replace_term_to_mask(term: str) -> str:
    return re.sub(
        r'\w',
        lambda m: m.group() if random.randint(0, 1) else '?',
        term,
    )


class RequestTermByMaskAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_request_term_by_sample() and text != CANCEL

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        if user.is_term_right(text):
            user.update_repetition(3)
            viewer.view(user.id, RIGHT)
            RequestTermByDefinitionAction().do(viewer, user, '')
        else:
            term = user.request_term_by_mask()
            viewer.view(user.id, ENTER_TERM_WITH_MASK)
            viewer.view(user.id, replace_term_to_mask(term), keyboards.get_cancel())
