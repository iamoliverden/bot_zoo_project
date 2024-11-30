# ZoomZoomMSK Telegram Bot

This project is an unofficial Telegram bot built using Django and Telegram Bot API. The bot, ZoomZoomMSK, helps users discover their "totem animal" from the Moscow Zoo by answering a set of fun questions.

While this project is unofficial, it demonstrates our ability to develop interactive and engaging applications by integrating a Django backend with a Telegram bot.

## Features
A conversational quiz to determine your totem animal.

Integration with a Django backend to store questions, answers, and animals.
Displays the selected totem animal’s name and picture at the end of the quiz.

## Getting Started

To run this project:

Install dependencies: Make sure you have a virtual environment and install the dependencies listed in the requirements.txt file. You can do this by running:

```bash
pip install -r requirements.txt
```

Run the bot: To start the Telegram bot, run the following command:

```bash
python manage.py run_bot
```

Run the Django server: If you want to access the Django admin panel or make changes to the backend, run:

```bash
python manage.py runserver
```

## Set up your Telegram Bot:

The bot is named ZoomZoomMSK, but you can create a different bot for this purpose.
To do so, create a new bot using the BotFather and add the bot's token to the key.py file.
Database: The project uses the provided database. Do not recreate the database as it already contains the correct data for the project to function properly.

## Important Notes:

The bot messages, questions, and answers are in Spanish.
The bot interacts with users to help them discover which animal is their totem, with a fun and engaging quiz.
Make sure to store sensitive information, like the bot token, securely and not in public repositories.

## License
This project is open-source. Feel free to contribute or customize it for your own purposes.