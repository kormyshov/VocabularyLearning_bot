import keyboards
from logging_decorator import logger
from abstract_base import AbstractBase
from abstract_viewer import AbstractViewer
from user import User
import constants


class Controller:
    def __init__(self, database: AbstractBase, viewer: AbstractViewer):
        self.database = database
        self.viewer = viewer

    @logger
    def look_sets(self, user: User) -> None:
        is_empty = True
        for user_set in user.get_sets():
            self.viewer.view(user.id, '{}. {}'.format(user_set.id, user_set.name))
            is_empty = False
        if is_empty:
            self.viewer.view(user.id, constants.YOU_DONT_HAVE_SET)

    @logger
    def request_to_look_set_info(self, user: User) -> None:
        user_set_names = user.request_to_look_set_info()
        keyboard = keyboards.get_sets(user_set_names)
        if len(keyboard) == 1:
            user.go_to_main_menu()
            self.viewer.view(user.id, constants.YOU_DONT_HAVE_SET, keyboards.get_main_menu())
        else:
            self.viewer.view(user.id, constants.SELECT_SET, keyboard)

    @logger
    def look_set_info(self, user: User, set_name: str) -> None:
        pass

    @logger
    def go_to_main_menu(self, user: User) -> None:
        user.go_to_main_menu()
        self.viewer.view(user.id, constants.MENU, keyboards.get_main_menu())

    @logger
    def operate(self, user_id: str, text: str):
        user = User(user_id, self.database)

        if text == constants.LOOK_SETS:
            self.look_sets(user)
        elif text == constants.LOOK_SET_INFO:
            self.request_to_look_set_info(user)
        elif text == constants.BACK:
            self.go_to_main_menu(user)
        else:
            if user.is_request_to_look_set_info():
                self.look_set_info(user, text)

        user.save()
