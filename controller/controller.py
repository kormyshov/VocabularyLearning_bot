from logging_decorator import logger
from abstract_base import AbstractBase
from abstract_viewer import AbstractViewer
from user import User
from look_sets_action import LookSetsAction
from request_to_look_set_info_action import RequestToLookSetInfoAction
from request_to_add_set_action import RequestToAddSetAction
from request_to_delete_set_action import RequestToDeleteSetAction
from request_to_add_exist_set_action import RequestToAddExistSetAction
from request_to_add_new_set_action import RequestToAddNewSetAction
from go_to_main_menu_action import GoToMainMenuAction
from add_exist_set_action import AddExistSetAction
from add_new_set_action import AddNewSetAction
from look_set_info_action import LookSetInfoAction
from delete_set_action import DeleteSetAction


class Controller:

    actions = (
        LookSetsAction(),
        RequestToLookSetInfoAction(),
        RequestToAddSetAction(),
        RequestToDeleteSetAction(),
        RequestToAddExistSetAction(),
        RequestToAddNewSetAction(),
        GoToMainMenuAction(),
        AddExistSetAction(),
        AddNewSetAction(),
        LookSetInfoAction(),
        DeleteSetAction(),
    )

    def __init__(self, database: AbstractBase, viewer: AbstractViewer):
        self.database = database
        self.viewer = viewer

    @logger
    def operate(self, user_id: str, text: str):
        user = User(user_id, self.database)
        user.load()

        for action in self.actions:
            if action.check(user, text):
                action.do(self.viewer, user, text)
                break

        user.save()
