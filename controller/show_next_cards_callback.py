from logging_decorator import logger
from controller.abstract_callback import AbstractCallback
from abstract_viewer import AbstractViewer
from user import User
from set_info import PageOfCards


class ShowNextCardsCallback(AbstractCallback):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_look_set_info()

    @logger
    def do(self, viewer: AbstractViewer, user: User, message_id: int, text: str) -> None:
        page: PageOfCards = user.show_all_cards(int(text))
        navigator = {0, max(0, page.page - 1), page.page, min(page.page + 1, page.max_page - 1), page.max_page - 1}
        viewer.edit(
            user.id,
            message_id,
            '<b>Page {} of {}</b>\n\n{}'.format(
                page.page,
                page.max_page - 1,
                '\n'.join(page.terms),
            ),
            map(str, sorted(list(navigator))),
            True,
        )
