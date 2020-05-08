import os
from config import TOKEN_DEV
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from requests import get, post, delete
from send_email import send_email

api_url = 'http://localhost:5000'

REQUEST_KWARGS = {
    'proxy_url': 'socks4://198.50.177.44:44699'
}


def start(update, context):
    reply_keyboard = [['/usual']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Выберите режим',
                              reply_markup=markup)


def usual(update, context):
    context.user_data['data'] = {}
    update.message.reply_text('Пожалуйста, введите название вашей истории')
    return 1


def title(update, context):
    print('here')
    context.user_data['data']['title'] = update.message.text
    update.message.reply_text('Пожалуйста, введите текст истории')
    return 2


def text(update, context):
    context.user_data['data']['text'] = update.message.text
    update.message.reply_text('Пожалуйста, введите ответ на историю')
    return 3


def answer(update, context):
    context.user_data['data']['answer'] = update.message.text
    update.message.reply_text('Пожалуйста, введите слова очевидцев')
    return 4


def spectator(update, context):
    context.user_data['data']['spectator'] = update.message.text
    update.message.reply_text('Пожалуйста, введите мнение коллег')
    return 5


def opinion(update, context):
    context.user_data['data']['opinion'] = update.message.text
    update.message.reply_text('Пожалуйста, введите api, которое используется в истории')
    return 6


def api(update, context):
    context.user_data['data']['api'] = update.message.text
    update.message.reply_text('Пожалуйста, введите текст, согласующийся с api')
    return 7


def proof(update, context):
    context.user_data['data']['proof'] = update.message.text
    update.message.reply_text('Пожалуйста, введите пояснение к объекту api(если такого нет - None)')
    return 8


def api_message(update, context):
    context.user_data['data']['api_message'] = update.message.text
    message = ['Пожалуйста, введите 5 ответов на историю', 'Ответы должны быть разделены _',
               'Один из ответов должен быть правильным(тем, что вы указали ранее)']
    update.message.reply_text('\n'.join(message))
    return 9


def answer_choice(update, context):
    context.user_data['data']['answer_choice'] = update.message.text
    reply_keyboard = [['yes'],
                      ['no']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Процесс создания истории завершен. Хотите отправить ее на модерацию?',
                              reply_markup=markup)
    return 10


def moderation(update, context):
    if update.message.text == 'no':
        reply_keyboard = [['/usual']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text('Попробуйте заново!', reply_markup=markup)
    else:
        message = list(context.user_data['data'].values())
        send_email('\n'.join(message).encode('utf-8'))
        update.message.reply_text('История успешно добавлена!')
    return ConversationHandler.END


def dev(update, context):
    f = update.message.document
    file_name = str(f.get_file().file_path).split('/')[-1]
    print(file_name)
    f.get_file().download()
    file = open(file_name, encoding='utf-8')
    temp = []
    for line in file:
        line = line.replace('\n', '')
        if line == '---':
            # добавление истории
            message = temp[7]
            if message == 'None':
                message = None
            print(temp)
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

    dp.add_handler(MessageHandler(Filters.document, dev, pass_user_data=True))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('usual', usual, pass_user_data=True)],

        states={
            1: [MessageHandler(Filters.text, title, pass_user_data=True)],
            2: [MessageHandler(Filters.text, text, pass_user_data=True)],
            3: [MessageHandler(Filters.text, answer, pass_user_data=True)],
            4: [MessageHandler(Filters.text, spectator, pass_user_data=True)],
            5: [MessageHandler(Filters.text, opinion, pass_user_data=True)],
            6: [MessageHandler(Filters.text, api, pass_user_data=True)],
            7: [MessageHandler(Filters.text, proof, pass_user_data=True)],
            8: [MessageHandler(Filters.text, api_message, pass_user_data=True)],
            9: [MessageHandler(Filters.text, answer_choice, pass_user_data=True)],
            10: [MessageHandler(Filters.text, moderation, pass_user_data=True)]

        },
        fallbacks=[]
    )
    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
