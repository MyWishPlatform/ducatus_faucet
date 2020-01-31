import telebot
from app.queries import *

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text=bot_message)


@bot.message_handler()
def transaction_request(message):
    transaction_response = main_process(message.text, str(message.chat.id))
    bot.send_message(chat_id=message.chat.id, text=transaction_response.replace(',', '\n'))



if __name__ == '__main__':
    bot.polling()
