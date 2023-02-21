from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import BACK, SHOW_ALL_CARDS
from set_info import PageOfCards
from keyboards import get_mutable_set_info_menu, get_immutable_set_info_menu
from controller.utils import parse_set_id_from_button_name, validate_set_id_in_button_name


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
        # info: SetInfo = user.look_set_info(
        #     parse_set_id_from_button_name(text) if validate_set_id_in_button_name(text) else user.set_id
        # )
        # if info is not None:
        #     viewer.view(
        #         user.id,
        #         '<b>{}</b>\n\n{} cards\n{} cards to repeat\n{} cards are ready'.format(
        #             info.name,
        #             info.stat.count,
        #             info.stat.count_to_repeat,
        #             info.stat.count_finished,
        #         ),
        #         get_mutable_set_info_menu() if info.is_mutable else get_immutable_set_info_menu()
        #     )
        # else:
        #     viewer.view(user.id, THERE_IS_NO_SET)
