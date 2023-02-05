from keyboards import get_main_menu
from constants import ONBOARDING
from database import Database
from controller.controller import Controller
from telegram_viewer import TelegramViewer, bot


@bot.message_handler(commands=['start'])
def start_message(message):
    TelegramViewer().view(message.chat.id, ONBOARDING, get_main_menu())


@bot.message_handler(content_types='text')
def message_reply(message):
    db = Database()
    viewer = TelegramViewer()
    Controller(db, viewer).operate(str(message.chat.id), message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_reply(call):
    print(call)
