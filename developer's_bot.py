from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from requests import get, post, delete
from config import TOKEN_DEV
import os

api_url = 'http://localhost:5000'

REQUEST_KWARGS = {
    'proxy_url': 'socks4://62.43.206.20:48714'
}


def start(update, context):
    reply_keyboard = [['/usual'],
                      ['/dev']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Все работает')


def usual(update, context):
    pass


def dev(update, context):
    f = update.message.document
    file_name = str(f.get_file().file_path).split('/')[-1]
    print(file_name)
    f.get_file().download()
    file = open(file_name)
    temp = []
    for line in file:
        line = line.replace('\n', '')
        if line == '---':
            # добавление истории
            message = temp[7]
            if message == 'None':
                message = None
            post(f'{api_url}/api/stories',
                 json={'id': None,
                       'title': temp[0],
                       'text': temp[1],
                       'answer': temp[2],
                       'spectator': temp[3],
                       'opinion': temp[4],
                       'api': temp[5],
                       'proof': temp[6],
                       'api_message': message,
                       'answer_choice': temp[8]})
            temp = []
        else:
            temp.append(line)
    file.close()
    os.remove(file_name)

    update.message.reply_text('Истории добавлены')


def main():
    updater = Updater(TOKEN_DEV, use_context=True, request_kwargs=REQUEST_KWARGS)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start',
                                  start,
                                  pass_user_data=True))
    dp.add_handler(CommandHandler('usual',
                                  usual,
                                  pass_user_data=True))
    dp.add_handler(CommandHandler('dev',
                                  dev,
                                  pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.document, dev, pass_user_data=True))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
