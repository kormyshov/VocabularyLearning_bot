from abc import ABC, abstractmethod
from user import User
from abstract_viewer import AbstractViewer


class AbstractCallback(ABC):
    @abstractmethod
    def check(self, user: User, text: str) -> bool:
        pass

    @abstractmethod
    def do(self, viewer: AbstractViewer, user: User, message_id: int, text: str) -> None:
        pass
