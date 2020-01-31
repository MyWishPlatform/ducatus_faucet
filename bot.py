import telebot
from settings_local import bot_token, bot_message, service_url, service_port
import requests
from app.handlers import main_process

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text=bot_message)


@bot.message_handler()
def transaction_request(message):
    transaction_response = main_process(message.text, message.chat.id)
    response_data = transaction_response.content.decode()
    bot.send_message(chat_id=message.chat.id, text=response_data.replace(',', '\n'))


if __name__ == '__main__':
    bot.polling()
