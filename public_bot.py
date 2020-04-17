from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from requests import get, post, delete
from load_image_from_yandex import load_image
from config import TOKEN
import os
import random

api_url = 'http://localhost:5000'

REQUEST_KWARGS = {
    'proxy_url': 'socks4://151.80.201.162:1080'
}


def start(update, context):
    context.user_data['in_progress'] = []
    context.user_data['active_story'] = 0
    context.user_data['story_dict'] = {}

    stories = get(f'{api_url}/api/stories').json()['stories']

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
    story = get(f'{api_url}/api/stories/{number}').json()['stories']
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
        context.user_data['story_dict'][number]['proof'] = True
        story = get(f'{api_url}/api/stories/{number}').json()['stories']
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
            os.remove(map_file)
    remains = context.user_data['story_dict'][number]
    reply = []
    if not remains['proof']:
        reply.append('У вас осталась 1 улика \n')
    if not remains['spectator']:
        reply.append('У вас осталось 1 мнение очевидцев \n')
    if not remains['opinion']:
        reply.append('У вас остался 1 диалог с коллегами \n')
    if len(reply) == 0:
        reply.append('У вас больше нет подсказок')
    update.message.reply_text(''.join(reply))


def spectator(update, context):
    number = context.user_data['active_story']
    if context.user_data['story_dict'][number]['spectator']:
        update.message.reply_text('Вы опросили всех очевидцев')
    else:
        story = get(f'{api_url}/api/stories/{number}').json()['stories']
        phrase = story['spectator']
        begins = ['Вам сообщили, что ', 'Вы узнали, что ', 'Опрос показал, что ',
                  'Очевидцы рассказали, что ']
        context.user_data['story_dict'][number]['spectator'] = True
        update.message.reply_text(f'{random.choice(begins)}{phrase}')
    remains = context.user_data['story_dict'][number]
    reply = []
    if not remains['proof']:
        reply.append('У вас осталась 1 улика \n')
    if not remains['spectator']:
        reply.append('У вас осталось 1 мнение очевидцев \n')
    if not remains['opinion']:
        reply.append('У вас остался 1 диалог с коллегами \n')
    if len(reply) == 0:
        reply.append('У вас больше нет подсказок')
    update.message.reply_text(''.join(reply))


def opinion(update, context):
    number = context.user_data['active_story']
    if context.user_data['story_dict'][number]['opinion']:
        update.message.reply_text('Вы опросили всех коллег')
    else:
        story = get(f'{api_url}/api/stories/{number}').json()['stories']
        phrase = story['opinion']
        begins = ['Коллеги думают, что ', 'Вы узнали, что ', 'Ваши друзья думают, что ',
                  'Профессионалы рассказали, что ']
        context.user_data['story_dict'][number]['opinion'] = True
        update.message.reply_text(f'{random.choice(begins)}{phrase}')
    remains = context.user_data['story_dict'][number]
    reply = []
    if not remains['proof']:
        reply.append('У вас осталась 1 улика \n')
    if not remains['spectator']:
        reply.append('У вас осталось 1 мнение очевидцев \n')
    if not remains['opinion']:
        reply.append('У вас остался 1 диалог с коллегами \n')
    if len(reply) == 0:
        reply.append('У вас больше нет подсказок')
    update.message.reply_text(''.join(reply))


def answer(update, context):
    number = context.user_data['active_story']
    story = get(f'{api_url}/api/stories/{number}').json()['stories']['answer_choice'].split('_')

    reply_keyboard = [['/yes'],
                      ['no']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    begins = ['Как вы думаете, ', 'По вашему мнению, ', 'Вы считаете, что ', 'Вы думаете, что ']
    update.message.reply_text(
        f'{random.choice(begins)}{story[0]}?',
        reply_markup=markup
    )
    return 1


def first_response(update, context):
    print(1)
    update.message.reply_text('Следующий вопрос...')


def second_response(update, context):
    pass


def third_response(update, context):
    pass


def agree(update, context):
    return ConversationHandler.END


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

    dp.add_handler(CommandHandler('spectator',
                                  spectator,
                                  pass_user_data=True))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('answer', answer, pass_user_data=True)],

        states={
            1: [MessageHandler(Filters.text, first_response)],
            2: [MessageHandler(Filters.text, second_response)]
        },

        fallbacks=[CommandHandler('yes', agree)]
    )

    dp.add_handler(CommandHandler('yes', agree))
    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
