from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import BACK
from keyboards import get_look_set_info
from card_info import CardInfo


class AddCardAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_request_to_add_sample() and text != BACK[user.language]

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        sample_id = user.add_sample(text)
        card_id = user.add_card(user.set_id, user.term_id, user.definition_id, sample_id)
        info: CardInfo = user.look_card_info(card_id)
        viewer.view_card(user.id, info, get_look_set_info(user.language))
