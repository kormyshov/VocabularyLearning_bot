from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import BACK, CARD_HAS_BEEN_DELETED, THERE_IS_NO_CARD
from controller.look_set_info_action import LookSetInfoAction


class DeleteCardAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_request_to_delete_card() and text != BACK

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        if user.delete_card(text):
            viewer.view(user.id, CARD_HAS_BEEN_DELETED)
            LookSetInfoAction().do(viewer, user, "")
        else:
            viewer.view(user.id, THERE_IS_NO_CARD)
