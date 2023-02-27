from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import BACK, SHOW_ALL_CARDS
from set_info import PageOfCards


class ShowAllCardsAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_look_set_info() and text == SHOW_ALL_CARDS

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        page: PageOfCards = user.show_all_cards(0)
        navigator = {0, min(page.page + 1, page.max_page - 1), min(page.page + 2, page.max_page - 1), page.max_page - 1}
        viewer.view(
            user.id,
            '<b>Page {} of {}</b>\n\n{}'.format(
                page.page,
                page.max_page - 1,
                '\n'.join(page.terms),
            ),
            map(str, sorted(list(navigator))),
            True,
        )
