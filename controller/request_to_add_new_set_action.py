from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import NEW_SET, ENTER_SET_NAME
import keyboards


class RequestToAddNewSetAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_request_to_add_set() and text == NEW_SET['en']

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        user.request_to_add_new_set()
        viewer.view(user.id, ENTER_SET_NAME['en'], keyboards.get_back())
