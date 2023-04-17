from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import DELETE_CARD, ENTER_TERM
import keyboards


class RequestToDeleteCardAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_look_set_info() and text == DELETE_CARD['en']

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        user.request_to_delete_card()
        viewer.view(user.id, ENTER_TERM['en'], keyboards.get_back())
