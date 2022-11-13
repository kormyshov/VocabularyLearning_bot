from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import BACK, LEARN, SET_IS_EMPTY, ENTER_TERM_WITH_DEFINITION
import keyboards
from controller.utils import parse_set_id_from_button_name, validate_set_id_in_button_name


class RequestTermByDefinitionAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return (
            (user.is_look_set_info() and text == LEARN) or
            (user.is_request_to_learn_set() and text != BACK)
        )

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        definition = user.request_term_by_definition(
            parse_set_id_from_button_name(text) if validate_set_id_in_button_name(text) else user.set_id
        )
        if definition is not None:
            viewer.view(user.id, ENTER_TERM_WITH_DEFINITION)
        else:
            viewer.view(user.id, SET_IS_EMPTY)
