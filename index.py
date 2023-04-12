import telebot
import logging
from main import bot


def handler(event, _):
    print('ok 1')
    logging.getLogger().setLevel(logging.INFO)
    print('ok 2')
    root_handler = logging.getLogger().handlers[0]
    print('ok 3')
    root_handler.setFormatter(logging.Formatter(
        '[%(levelname)s]\t%(request_id)s\t%(name)s\t%(message)s\n'
    ))
    print('ok 4')
    logging.info('Program started')
    print('ok 5')

    message = telebot.types.Update.de_json(event['body'])
    print('ok 6')
    bot.process_new_updates([message])
    print('ok 7')
    return {
        'statusCode': 200,
        'body': '!',
    }
