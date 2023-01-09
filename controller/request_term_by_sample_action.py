import re
from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import CANCEL, IT_IS_USED_IN, RIGHT, WITHOUT_SAMPLE, SECOND_ATTEMPT
import keyboards
from controller.request_term_by_definition_action import RequestTermByDefinitionAction


def replace_term_to_stars(sample: str) -> str:
    return re.sub(
        r'\[.+?\]',
        lambda m: re.sub(r'\S', '*', m.group().strip('[]')),
        sample,
    )


class RequestTermBySampleAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_request_term_by_definition() and text != CANCEL

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        if user.is_term_right(text):
            user.update_repetition(5)
            viewer.view(user.id, RIGHT)
            sample = user.get_sample_of_current_card()
            viewer.view(user.id, IT_IS_USED_IN)
            viewer.view(user.id, sample.replace('[', '').replace(']', ''))
            RequestTermByDefinitionAction().do(viewer, user, '')
        else:
            sample = user.request_term_by_sample()
            if sample != WITHOUT_SAMPLE:
                viewer.view(user.id, IT_IS_USED_IN)
                viewer.view(user.id, replace_term_to_stars(sample), keyboards.get_cancel())
            else:
                viewer.view(user.id, SECOND_ATTEMPT, keyboards.get_cancel())
