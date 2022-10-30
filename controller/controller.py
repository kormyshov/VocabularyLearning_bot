from typing import Tuple
from logging_decorator import logger
from abstract_base import AbstractBase
from abstract_viewer import AbstractViewer
from user import User
from controller.abstract_action import AbstractAction
from controller.look_sets_action import LookSetsAction
from controller.request_to_look_set_info_action import RequestToLookSetInfoAction
from controller.request_to_add_set_action import RequestToAddSetAction
from controller.request_to_delete_set_action import RequestToDeleteSetAction
from controller.request_to_add_exist_set_action import RequestToAddExistSetAction
from controller.request_to_add_new_set_action import RequestToAddNewSetAction
from controller.go_to_main_menu_action import GoToMainMenuAction
from controller.add_exist_set_action import AddExistSetAction
from controller.add_new_set_action import AddNewSetAction
from controller.look_set_info_action import LookSetInfoAction
from controller.delete_set_action import DeleteSetAction
from controller.request_to_add_term_action import RequestToAddTermAction
from controller.request_to_add_definition_action import RequestToAddDefinitionAction
from controller.request_to_add_sample_action import RequestToAddSampleAction


class Controller:

    actions: Tuple[AbstractAction] = (
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
        RequestToAddTermAction(),
        RequestToAddDefinitionAction(),
        RequestToAddSampleAction(),
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
