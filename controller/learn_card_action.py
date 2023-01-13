from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import CANCEL, RIGHT, IT_WAS
import keyboards
from controller.request_term_by_definition_action import RequestTermByDefinitionAction


class LearnCardAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_request_term_by_mask() and text != CANCEL

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        if user.is_term_right(text):
            user.update_repetition(2)
            viewer.view(user.id, RIGHT)
        else:
            user.update_repetition(0)
            card = user.get_card_info(user.card_id)
            viewer.view(user.id, IT_WAS)
            viewer.view_card(user.id, card, keyboards.get_cancel())
        RequestTermByDefinitionAction().do(viewer, user, '')
