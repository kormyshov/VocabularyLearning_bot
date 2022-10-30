from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import BACK, ENTER_DEFINITION
from keyboards import get_empty


class RequestToAddDefinitionAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return (
            (user.is_request_to_add_term() and text != BACK) or
            (user.is_request_to_add_sample() and text == BACK)
        )

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        term_id = user.add_term(text)
        user.request_to_add_definition(term_id)
        viewer.view(user.id, ENTER_DEFINITION.format(text), get_empty())
