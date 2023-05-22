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
    def rand():
        nonlocal n, i, k
        r = random.randint(0, 999_999)
        t = (n / 2 - k) / (n / 2) / ((n - i) ** 0.33) * 1_000_000
        i += 1
        if r < t:
            k += 1
            return 1
        return 0

    n = len(re.findall(r'\w', term))
    i, k = 0, 0
    return re.sub(
        r'\w',
        lambda m: m.group() if rand() else '?',
        term,
    )


class RequestTermByMaskAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_request_term_by_sample() and text != CANCEL[user.language]

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        if user.is_term_right(text):
            user.update_repetition(3)
            viewer.view(user.id, RIGHT[user.language])
            card = user.get_card_info(user.card_id)
            viewer.view_card(user.id, card)
            RequestTermByDefinitionAction().do(viewer, user, '')
        else:
            term = user.request_term_by_mask()
            viewer.view(user.id, ENTER_TERM_WITH_MASK[user.language])
            viewer.view(user.id, replace_term_to_mask(term), keyboards.get_cancel(user.language))
