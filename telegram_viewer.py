import os
import telebot
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from abstract_viewer import AbstractViewer, Iterable, Optional, CardInfo


bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))


class TelegramViewer(AbstractViewer):
    def __init__(self):
        pass

    def view(self, player_id: str, message: str, keyboard: Optional[Iterable[str]] = None) -> None:
        if keyboard is not None:
            bot.send_message(player_id, message, reply_markup=self.get_keyboard(keyboard), parse_mode='HTML')
        else:
            bot.send_message(player_id, message)

    def get_keyboard(self, actions: Iterable[str]) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for action in actions:
            keyboard.add(KeyboardButton(action))
        return keyboard

    def view_card(self, player_id: str, card: CardInfo, keyboard: Optional[Iterable[str]] = None) -> None:
        if card.sample is not None:
            self.view(
                player_id,
                '<b>{}</b>\n\n{}\n\n{}'.format(
                    card.term,
                    card.definition,
                    card.sample.replace('[', '<b>').replace(']', '</b>'),
                ),
                keyboard,
            )
        else:
            self.view(
                player_id,
                '<b>{}</b>\n\n{}\n'.format(card.term, card.definition),
                keyboard,
            )
