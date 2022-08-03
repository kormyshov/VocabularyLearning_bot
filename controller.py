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
            self.viewer.view(user.id, '{}. {}'.format(user_set.id, str(user_set.name)))
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
    def request_to_add_set(self, user: User) -> None:
        if user.request_to_add_set():
            self.viewer.view(user.id, constants.DO_YOU_WANT_TO_CREATE_OR_ADD_EXIST_SET, keyboards.get_add_set_menu())
        else:
            self.viewer.view(user.id, constants.YOU_HAVE_MAX_SET_COUNT, keyboards.get_main_menu())

    @logger
    def request_to_add_exist_set(self, user: User) -> None:
        user.request_to_add_exist_set()
        self.viewer.view(user.id, constants.ENTER_ID_OF_SET, keyboards.get_back())

    @logger
    def request_to_add_new_set(self, user: User) -> None:
        user.request_to_add_new_set()
        self.viewer.view(user.id, constants.ENTER_SET_NAME, keyboards.get_back())

    @logger
    def add_exist_set(self, user: User, set_id: str) -> None:
        if user.add_exist_set(int(set_id)):
            self.viewer.view(user.id, constants.SET_HAS_BEEN_ADDED)
            self.go_to_main_menu(user)
        else:
            self.viewer.view(user.id, constants.THERE_IS_NO_SET)

    @logger
    def add_new_set(self, user: User, set_name: str) -> None:
        user.add_new_set(set_name)
        self.viewer.view(user.id, constants.SET_HAS_BEEN_CREATED)
        self.go_to_main_menu(user)

    @logger
    def go_to_main_menu(self, user: User) -> None:
        user.go_to_main_menu()
        self.viewer.view(user.id, constants.MENU, keyboards.get_main_menu())

    @logger
    def operate(self, user_id: str, text: str):
        user = User(user_id, self.database)
        user.load()

        if user.is_main_menu():
            if text == constants.LOOK_SETS:
                self.look_sets(user)
            elif text == constants.LOOK_SET_INFO:
                self.request_to_look_set_info(user)
            elif text == constants.ADD_SET:
                self.request_to_add_set(user)
        elif user.is_request_to_add_set():
            if text == constants.EXIST_SET:
                self.request_to_add_exist_set(user)
            elif text == constants.NEW_SET:
                self.request_to_add_new_set(user)
            elif text == constants.BACK:
                self.go_to_main_menu(user)
        elif user.is_request_to_add_exist_set():
            if text == constants.BACK:
                self.request_to_add_set(user)
            else:
                self.add_exist_set(user, text)
        elif user.is_request_to_add_new_set():
            if text == constants.BACK:
                self.request_to_add_set(user)
            else:
                self.add_new_set(user, text)
        elif user.is_request_to_look_set_info():
            if text == constants.BACK:
                self.go_to_main_menu(user)
            else:
                self.look_set_info(user, text)
        else:
            pass

        user.save()
