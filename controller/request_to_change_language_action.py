from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import CHANGE_LANGUAGE, CHOOSE_LANGUAGE
import keyboards


class RequestToChangeLanguageAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return (
            user.is_main_menu() and text == CHANGE_LANGUAGE['en']
        )

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        user.request_to_change_language()
        viewer.view(user.id, CHOOSE_LANGUAGE['en'], keyboards.get_ui_languages())
