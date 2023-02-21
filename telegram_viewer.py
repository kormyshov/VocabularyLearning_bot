import os
import telebot
from telebot.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)
from abstract_viewer import AbstractViewer, Iterable, Optional, CardInfo


bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))


class TelegramViewer(AbstractViewer):
    def __init__(self):
        pass

    def view(
        self,
        player_id: str,
        message: str,
        keyboard: Optional[Iterable[str]] = None,
        is_inline: Optional[bool] = False
    ) -> None:
        if keyboard is not None:
            bot.send_message(player_id, message, reply_markup=self.get_keyboard(keyboard, is_inline), parse_mode='HTML')
        else:
            bot.send_message(player_id, message, parse_mode='HTML')

    def get_keyboard(self, actions: Iterable[str], is_inline: bool) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True) if not is_inline else InlineKeyboardMarkup()
        keyboard.add(*[
            KeyboardButton(action) if not is_inline else InlineKeyboardButton(action, callback_data=action)
            for action in actions
        ])
        # for action in actions:
        #     keyboard.add(
        #         KeyboardButton(action) if not is_inline else InlineKeyboardButton(action, callback_data=action)
        #     )
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

    def edit(
        self,
        player_id: str,
        message_id: int,
        message: str,
        keyboard: Optional[Iterable[str]] = None,
        is_inline: Optional[bool] = False
    ) -> None:
        bot.edit_message_text(
            message,
            player_id,
            message_id,
            reply_markup=self.get_keyboard(keyboard, is_inline),
            parse_mode='HTML',
        )
