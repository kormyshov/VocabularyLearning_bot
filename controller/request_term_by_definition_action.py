from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import BACK, LEARN, SET_IS_EMPTY, ENTER_TERM_WITH_DEFINITION, ALL_TERMS_REPEATED
import keyboards
from controller.utils import parse_set_id_from_button_name, validate_set_id_in_button_name
from abstract_base import SetIsEmpty, AllTermsRepeated


class RequestTermByDefinitionAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return (
            (user.is_look_set_info() and text == LEARN['en']) or
            (user.is_request_to_learn_set() and text != BACK['en'])
        )

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        try:
            definition = user.request_term_by_definition(
                parse_set_id_from_button_name(text) if validate_set_id_in_button_name(text) else user.set_id
            )
            viewer.view(user.id, ENTER_TERM_WITH_DEFINITION['en'])
            viewer.view(user.id, definition, keyboards.get_cancel())
        except SetIsEmpty:
            viewer.view(user.id, SET_IS_EMPTY['en'])
        except AllTermsRepeated:
            viewer.view(user.id, ALL_TERMS_REPEATED['en'])
