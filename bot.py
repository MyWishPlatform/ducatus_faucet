import telebot
from settings_local import bot_token, bot_message, service_url, service_port
import requests

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text=bot_message)


@bot.message_handler()
def transaction_request(message):
    request_data = {'address': message.text}
    transaction_response = requests.post(f'http://{service_url}:{service_port}/api/request/', json=request_data)
    response_data = transaction_response.content.decode()
    bot.send_message(chat_id=message.chat.id, text=response_data.replace(',', '\n'))


if __name__ == '__main__':
    bot.polling()
