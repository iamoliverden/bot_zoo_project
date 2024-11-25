# bot.py

import time
from telebot import TeleBot
from django.conf import settings
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from .models import Question, Animal

# Bot initialization
bot = TeleBot(settings.TOKEN, threaded=False)

# Store answers and results in memory (no need for the User model)
result = {}  # To store answers by chat_id
animal_result = {}  # To store selected animals for each chat_id


# Start message - introduction to the test
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id

    # Send welcome message and options
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = KeyboardButton('\U0001F43E Prueba')
    markup.add(start_button)

    start_image = open('media/images/start_message.png', 'rb')
    start_message = f'¡Bienvenido! Pulsa en Prueba en el menú para descubrir cuál es tu animal tótem en el zoológico de Moscú'
    bot.send_photo(message.chat.id, start_image, caption=start_message, reply_markup=markup)


# Start the test and handle answers
@bot.message_handler(content_types=['text'])
def message_handler(message):
    chat_id = message.chat.id
    if message.text == '\U0001F43E Prueba':
        # Initialize the result storage for the user
        result[chat_id] = []
        animal_result[chat_id] = []

        # Start the first question
        ask_next_question(chat_id)


# Function to ask the next question
def ask_next_question(chat_id):
    # Determine the next question
    question_order = len(result[chat_id]) + 1  # Determine which question to ask based on number of answers
    try:
        question = Question.objects.get(order_in_test=question_order)
        bot.send_message(chat_id, f'\U0001F331 Pregunta {question.order_in_test}:\n{question.question}',
                         reply_markup=gen_markup(question.answers.all()))
    except Question.DoesNotExist:
        # If no more questions, process results
        get_result(chat_id)


# Generate buttons for answer options
def gen_markup(answers):
    markup = InlineKeyboardMarkup()
    InlineKeyboardMarkup()
    for answer in answers:
        markup.add(InlineKeyboardButton(f'{answer.answer}', callback_data=f'{answer.id}'
                                        ))
    return markup


# Handle user responses to answers
@bot.callback_query_handler(func=lambda call: True)
def callback_answers(call):
    chat_id = call.message.chat.id
    answer = call.data
    result[chat_id].append(answer)  # Store the user's answer

    # Find the corresponding animal for the answer
    question = Question.objects.get(order_in_test=len(result[chat_id]))
    animal = Animal.objects.filter(answers__contains=[answer]).first()  # Get animal related to this answer
    if animal:
        animal_result[chat_id].append(animal.name)

    # Ask the next question or finish if this is the last question
    if len(result[chat_id]) < Question.objects.count():
        ask_next_question(chat_id)
    else:
        get_result(chat_id)


# Calculate the final result and Totem Animal
def get_result(chat_id):
    # Calculate which animal got the most responses
    animal_counts = {animal: animal_result[chat_id].count(animal) for animal in set(animal_result[chat_id])}
    totem_animal = max(animal_counts, key=animal_counts.get)  # Get animal with the most counts

    # Send result message
    result_message = f"Tu animal tótem es: {totem_animal} 🦁\n\nPara más detalles, puedes contactar al zoológico de Moscú:\n" \
                     f"Teléfono: +7 (962) 971-38-75\nCorreo: zoofriends@moscowzoo.ru"
    bot.send_message(chat_id, result_message)

    # Offer option to retry
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    retry_button = KeyboardButton('\U0001F425 ¿Intentar de nuevo?')
    markup.add(retry_button)
    bot.send_message(chat_id, '¿Te gustaría intentarlo de nuevo?', reply_markup=markup)


# Run the bot
def main():
    bot.polling(none_stop=True)
