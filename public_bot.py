from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from requests import get, post, delete
from load_image_from_yandex import load_image

TOKEN = '1058008434:AAFrQo93WYtes4dzHiveCHi3VrWr2nStMjY'
REQUEST_KWARGS = {
    'proxy_url': 'socks4://151.80.201.162:1080'
}


def start(update, context):
    context.user_data['in_progress'] = []
    context.user_data['active_story'] = 0
    context.user_data['story_dict'] = {}

    stories = get('http://localhost:5000/api/stories').json()['stories']
    reply_keyboard = []
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    message = ['Добро пожаловать в Яндекс Детектив!',
               'Здесь Вы сможете погрузиться в жизнь настоящего детектива,',
               'разгадывая загадки и раскрывая преступления.',
               'Вам неизменно будут помогать Ваши коллеги и помощники',
               'Время начинать!']
    message_text = ['Вам доступны истории:']
    for x in stories:
        reply_keyboard.append([f"/story {x['id']}"])
        message_text.append(f"{x['id']} - {x['title']}")
    context.bot.send_photo(
        update.message.chat_id,
        open('static/img/detective_desk.jpg', 'rb'),
        caption='\n'.join(message)
    )
    update.message.reply_text(
        '\n'.join(message_text),
        reply_markup=markup
    )


def story(update, context):
    number = context.args[0]
    reply_keyboard = [['/proof'],
                      ['/spectator'],
                      ['/opinion']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    story = get(f'http://localhost:5000/api/stories/{number}').json()['stories']
    context.user_data['active_story'] = number
    context.user_data['in_progress'].append(number)
    context.user_data['story_dict'][number] = {'proof': False,
                                               'spectator': False,
                                               'opinion': False}
    help_message = ['/proof - посмотреть улики',
                    '/spectator - опросить очевидцев',
                    '/opinion - спросить мнение коллег']
    update.message.reply_text(story['text'])
    update.message.reply_text(
        '\n'.join(help_message),
        reply_markup=markup
    )


def proof(update, context):
    number = context.user_data['active_story']
    if context.user_data['story_dict'][number]['proof']:
        update.message.reply_text('У вас кончились улики')
    else:
        story = get(f'http://localhost:5000/api/stories/{number}').json()['stories']
        evidence = story['proof']
        api = story['api']
        # !!!!!ВАРИАНТЫ РАЗЛИЧНЫХ API!!!!!
        if api == 'image':
            map_file = load_image(evidence, update.message.chat_id)
            message = 'Вам стала доступна фотография с места преступления'
            context.bot.send_photo(
                update.message.chat_id,
                open(map_file, 'rb'),
                caption=message)
        # update.message.reply_text('Сейчас принесем улику...')


def main():
    updater = Updater(TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start',
                                  start,
                                  pass_user_data=True))

    dp.add_handler(CommandHandler('story',
                                  story,
                                  pass_args=True,
                                  pass_user_data=True))

    dp.add_handler(CommandHandler('proof',
                                  proof,
                                  pass_user_data=True))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
