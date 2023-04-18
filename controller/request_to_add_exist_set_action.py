from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import EXIST_SET, ENTER_ID_OF_SET
import keyboards


class RequestToAddExistSetAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_request_to_add_set() and text == EXIST_SET[user.language]

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        user.request_to_add_exist_set()
        viewer.view(user.id, ENTER_ID_OF_SET[user.language], keyboards.get_back(user.language))
