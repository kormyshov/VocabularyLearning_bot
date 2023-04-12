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
    print('8')
    db = Database()
    print('9')
    viewer = TelegramViewer()
    print('10')
    Controller(db, viewer).operate(str(message.chat.id), message.text)
    print('11')


@bot.callback_query_handler(func=lambda call: True)
def callback_reply(call):
    db = Database()
    viewer = TelegramViewer()
    Controller(db, viewer).callback(str(call.from_user.id), call.message.message_id, call.data)
    print(call)


# {
#     'id': '278772168642175487',
#     'from_user': {
#         'id': 64906703,
#         'is_bot': False,
#         'first_name': 'Михаил',
#         'username': 'kormyshov',
#         'last_name': None,
#         'language_code': 'ru',
#         'can_join_groups': None,
#         'can_read_all_group_messages': None,
#         'supports_inline_queries': None,
#         'is_premium': None,
#         'added_to_attachment_menu': None
#     },
#     'message': {
#         'content_type': 'text',
#         'id': 13665,
#         'message_id': 13665,
#         'from_user': <telebot.types.User object at 0x7f62db60a100>,
#         'date': 1675625318,
#         'chat': <telebot.types.Chat object at 0x7f62db60a130>,
#         'sender_chat': None,
#         'forward_from': None,
#         'forward_from_chat': None,
#         'forward_from_message_id': None,
#         'forward_signature': None,
#         'forward_sender_name': None,
#         'forward_date': None,
#         'is_automatic_forward': None,
#         'reply_to_message': None,
#         'via_bot': None,
#         'edit_date': None,
#           'has_protected_content': None,
#           'media_group_id': None,
#           'author_signature': None,
#           'text': 'Test message',
#           'entities': None,
#           'caption_entities': None,
#           'audio': None,
#           'document': None,
#           'photo': None,
#           'sticker': None,
#           'video': None,
#           'video_note': None,
#           'voice': None,
#           'caption': None,
#           'contact': None,
#           'location': None,
#           'venue': None,
#           'animation': None,
#           'dice': None,
#           'new_chat_member': None,
#           'new_chat_members': None,
#           'left_chat_member': None,
#           'new_chat_title': None,
#           'new_chat_photo': None,
#           'delete_chat_photo': None,
#           'group_chat_created': None,
#           'supergroup_chat_created': None,
#           'channel_chat_created': None,
#           'migrate_to_chat_id': None,
#           'migrate_from_chat_id': None,
#           'pinned_message': None,
#           'invoice': None,
#           'successful_payment': None,
#           'connected_website': None,
#           'reply_markup': <telebot.types.InlineKeyboardMarkup object at 0x7f62db60a0a0>,
#           'message_thread_id': None,
#           'is_topic_message': None,
#           'forum_topic_created': None,
#           'forum_topic_closed': None,
#           'forum_topic_reopened': None,
#           'has_media_spoiler': None,
#           'forum_topic_edited': None,
#           'general_forum_topic_hidden': None,
#           'general_forum_topic_unhidden': None,
#           'write_access_allowed': None,
#           'user_shared': None,
#           'chat_shared': None,
#           'json': {
#               'message_id': 13665,
#               'from': {
#                   'id': 5537399687,
#                   'is_bot': True,
#                   'first_name': 'Vocabulary learning',
#                   'username': 'VocabularyLearning_bot'
#               },
#               'chat': {
#                   'id': 64906703,
#                   'first_name': 'Михаил',
#                   'username': 'kormyshov',
#                   'type': 'private'
#               },
#               'date': 1675625318,
#               'text': 'Test message',
#               'reply_markup': {
#                   'inline_keyboard': [
#                       [{'text': 'inline_button', 'callback_data': 'inline_button'}],
#                       [{'text': 'Back', 'callback_data': 'Back'}]
#                   ]
#               }
#           }
#       },
#       'inline_message_id': None,
#       'chat_instance': '86785543992786735',
#       'data': 'inline_button',
# 'game_short_name': None,
# 'json': {
#     'id': '278772168642175487',
#     'from': {
#         'id': 64906703,
#         'is_bot': False,
#         'first_name': 'Михаил',
#         'username': 'kormyshov',
#         'language_code': 'ru'
#     },
#     'message': {
#         'message_id': 13665,
#         'from': {
#             'id': 5537399687,
#             'is_bot': True,
#             'first_name': 'Vocabulary learning',
#             'username': 'VocabularyLearning_bot'
#         },
#         'chat': {
#             'id': 64906703,
#             'first_name': 'Михаил',
#             'username': 'kormyshov',
#             'type': 'private'
#         },
#         'date': 1675625318,
#         'text': 'Test message',
#         'reply_markup': {
#             'inline_keyboard': [
#                 [{'text': 'inline_button', 'callback_data': 'inline_button'}],
#                 [{'text': 'Back', 'callback_data': 'Back'}]
#             ]
#         }
#     },
#     'chat_instance': '86785543992786735',
#     'data': 'inline_button'
# }
# }
