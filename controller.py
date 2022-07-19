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
    def operate(self, user_id: str, text: str):
        user = User(user_id, self.database)

        if text == constants.LOOK_SETS:
            self.look_sets(user)

        user.save()
