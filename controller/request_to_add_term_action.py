from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import ADD_CARD, ENTER_NEW_TERM, THIS_SET_HAS_MAX_CARD_COUNT, BACK
import keyboards


class RequestToAddTermAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return (
            (user.is_look_set_info() and text == ADD_CARD) or
            (user.is_request_to_add_definition() and text == BACK)
        )

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        if user.request_to_add_term():
            viewer.view(user.id, ENTER_NEW_TERM, keyboards.get_back())
        else:
            viewer.view(user.id, THIS_SET_HAS_MAX_CARD_COUNT)
