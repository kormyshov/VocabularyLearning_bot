from logging_decorator import logger
from controller.abstract_callback import AbstractCallback
from abstract_viewer import AbstractViewer
from user import User
from random import randint
from constants import BACK, SHOW_ALL_CARDS
from set_info import PageOfCards
from keyboards import get_mutable_set_info_menu, get_immutable_set_info_menu
from controller.utils import parse_set_id_from_button_name, validate_set_id_in_button_name


class ShowNextCardsCallback(AbstractCallback):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_look_set_info()

    @logger
    def do(self, viewer: AbstractViewer, user: User, message_id: int, text: str) -> None:
        page: PageOfCards = user.show_all_cards(int(text))
        viewer.edit(
            user.id,
            message_id,
            '<b>Page {} of {}</b>\n\n{}'.format(
                page.page,
                page.max_page - 1,
                '\n'.join(page.terms),
            ),
            [str(i) for i in range(page.max_page)],
            True,
        )
