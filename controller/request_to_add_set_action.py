from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import ADD_SET, DO_YOU_WANT_TO_CREATE_OR_ADD_EXIST_SET, YOU_HAVE_MAX_SET_COUNT, BACK
import keyboards


class RequestToAddSetAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return (
            (user.is_main_menu() and text == ADD_SET[user.language]) or
            (user.is_request_to_add_exist_set() and text == BACK[user.language]) or
            (user.is_request_to_add_new_set() and text == BACK[user.language])
        )

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        if user.request_to_add_set():
            viewer.view(
                user.id,
                DO_YOU_WANT_TO_CREATE_OR_ADD_EXIST_SET[user.language],
                keyboards.get_add_set_menu(user.language),
            )
        else:
            viewer.view(user.id, YOU_HAVE_MAX_SET_COUNT[user.language], keyboards.get_main_menu(user.language))
