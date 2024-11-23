# bot.py

import time

from django.conf import settings

from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from .models import User, Question, Animal


# Declaration of the bot variable
bot = TeleBot(settings.TOKEN, threaded=False)

# dictionary of user-selected answers result[chat_id]=[respuesta1, respuesta2]
result = {}

# dictionary of animals corresponding to selected answers animal_result[chat_id]=[animal1, animal2]
animal_result = {}


# getting user state
def get_user_state(chat_id):
    user = User.objects.filter(chat_id=chat_id).first()
    if user:
        return user.state


# updating user state
def update_user_state(chat_id, new_state):
    user = User.objects.filter(chat_id=chat_id).first()
    if user:
        user.state = new_state
        user.save()


# start message - creating user, introduction to the test
@bot.message_handler(commands=['start'])
def handle_start(message):
    user, created = User.objects.get_or_create(
        chat_id=message.chat.id,
        username=message.chat.username,
        state=1,
    )

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = KeyboardButton('\U0001F43E Prueba')
    markup.add(start_button)

    start_image = open('media/images/start_message.png', 'rb')
    start_message = f'¡Bienvenido, {user.username}! \n\n\U0001F331 Pulsa en Prueba en el menú para descubrir cuál ' \
                    f'es tu animal tótem en el zoológico de Moscú'

    bot.send_photo(message.chat.id, start_image, caption=start_message, reply_markup=markup)


# starting the test, handling start and result buttons
@bot.message_handler(content_types=['text'])
def message_handler(message):
    chat_id = message.chat.id
    result[chat_id] = []
    user = User.objects.filter(chat_id=chat_id).first()

    if message.text == '\U0001F43E Prueba':
        phone_gif = open('media/images/rotate_phone.gif', 'rb')
        phone_message = f'Gira tu teléfono para realizar la prueba'
        bot.send_animation(chat_id, phone_gif, caption=phone_message)
        time.sleep(3)
        ask_next_question(message.chat.id)

    elif message.text == '\U0001F999 Escribir a un empleado del zoológico':
        admin_chat_id = 350685069
        admin_message = f'El usuario @{user.username} quiere ponerse en contacto con usted.\n\n Resultado de la prueba:' \
                        f'\n <b>{user.test_result}</b>'
        bot.send_message(chat_id=admin_chat_id, text=admin_message, parse_mode='HTML')
        bot.send_message(chat_id, f'Ve al chat con nuestro empleado @dashazhu para continuar la conversación \U0001F43E')

    elif message.text == '\U0001F425 ¿Intentar de nuevo?':
        user.state = 1
        user.save()
        ask_next_question(chat_id)

    elif message.text == '\U0001F43E Dejar una reseña':
        bot_review_message = f'Envía tu reseña comenzando con "Reseña":\n<b>Reseña:</b> texto de la reseña\n\n' \
                             f'Por ejemplo,\nReseña: me gustaría ser un tigre...'
        bot.send_message(chat_id, bot_review_message, parse_mode='HTML')

    else:
        error_text = f'/start - inicio del bot \n\U0001F43E Prueba - iniciar la prueba \n\U0001F425 ¿Intentar de nuevo?' \
                     f'\n\U0001F999 Escribir a un empleado del zoológico \n\U0001F43E Dejar una reseña'
        bot.send_message(chat_id, f'Lamentablemente, no entendí lo que escribiste. Te recordaré mis comandos:\n\n{error_text}')


# displaying questions
def ask_next_question(chat_id):
    user = User.objects.filter(chat_id=chat_id).first()
    if user:
        user_state = get_user_state(chat_id=chat_id)
        question = Question.objects.get(order_in_test=user_state)
        bot.send_message(chat_id, f'\U0001F331 Pregunta {question.order_in_test}:\n{question.question}',
                         reply_markup=gen_markup(question.answers))


# answer options buttons
def gen_markup(answers):
    markup = InlineKeyboardMarkup()
    for answer in answers:
        answer = str(answer)
        markup.add(InlineKeyboardButton(
            f'{answer}', callback_data=answer[0:5]
        ))
    return markup


# processing the answer to the question
@bot.callback_query_handler(func=lambda call: True)
def callback_answers(call):
    chat_id = call.message.chat.id
    user = User.objects.filter(chat_id=chat_id).first()
    if user:
        user_state = get_user_state(chat_id)
        question_answers = Question.objects.filter(order_in_test=user_state).values_list('answers', flat=True)
        question_answers = question_answers[0]
        for answer in question_answers:
            if call.data in answer:
                result[chat_id].append(answer)
                if (user_state + 1) > Question.objects.count():
                    get_result(result[chat_id], chat_id)
                else:
                    new_state = user_state + 1
                    update_user_state(chat_id, new_state)
                    ask_next_question(chat_id)


# processing user's answers: from answer to animal
def get_result(user_answers, chat_id):
    animal_result[chat_id] = []
    animals = Animal.objects.all().values_list('answers', flat=True)
    for answer in user_answers:
        for animal_answers in animals:
            if answer in animal_answers:
                animal = Animal.objects.filter(answers__contains=[answer]).values('name').first()
                animal_result[chat_id].append(animal['name'])

    calculate_result(chat_id, animal_result[chat_id])


# obtaining the test result
def calculate_result(chat_id, result_animal):
    result_markup = ReplyKeyboardMarkup(resize_keyboard=True)

    replay_button = KeyboardButton('\U0001F425 ¿Intentar de nuevo?')

    result_inline = InlineKeyboardMarkup()
    result_markup.add(replay_button)

    main_result = {an: result_animal.count(an) for an in result_animal}
    max_value = max(main_result.values())
    for key in main_result:
        if main_result[key] == max_value:
            user = User.objects.filter(chat_id=chat_id).first()
            animal = Animal.objects.filter(name=key).first()
            user.test_result = animal
            user.save()
            bot.send_photo(chat_id, animal.animal, caption=f'{animal.test_result}', parse_mode='HTML',
                           reply_markup=result_markup)
            bot.send_message(chat_id, '¿Quieres compartir el bot en VK?', reply_markup=result_inline)
            break


def main():
    bot.polling(none_stop=True)
