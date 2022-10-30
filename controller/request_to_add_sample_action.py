from logging_decorator import logger
from controller.abstract_action import AbstractAction
from abstract_viewer import AbstractViewer
from user import User
from constants import BACK, ENTER_SAMPLE
from keyboards import get_empty


class RequestToAddSampleAction(AbstractAction):
    def __init__(self):
        pass

    def check(self, user: User, text: str) -> bool:
        return user.is_request_to_add_definition() and text != BACK

    @logger
    def do(self, viewer: AbstractViewer, user: User, text: str) -> None:
        definition_id = user.add_definition(text)
        user.request_to_add_sample(definition_id)
        viewer.view(user.id, ENTER_SAMPLE.format(text), get_empty())
