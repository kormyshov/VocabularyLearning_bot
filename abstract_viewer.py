from abc import ABC, abstractmethod
from typing import Iterable, Optional
from card_info import CardInfo


class AbstractViewer(ABC):
    @abstractmethod
    def view(
        self,
        player_id: str,
        message: str,
        keyboard: Optional[Iterable[str]] = None,
        is_inline: Optional[bool] = False
    ) -> None:
        pass

    @abstractmethod
    def view_card(self, player_id: str, card: CardInfo, keyboard: Optional[Iterable[str]] = None) -> None:
        pass

    @abstractmethod
    def edit(
        self,
        player_id: str,
        message_id: int,
        message: str,
        keyboard: Optional[Iterable[str]] = None,
        is_inline: Optional[bool] = False
    ) -> None:
        pass
