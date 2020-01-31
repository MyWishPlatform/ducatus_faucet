import telebot
from settings_local import *
import requests
from app.queries import *
from app.responses import *
from app.models import *

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text=bot_message)

def main_process(duc_address, ip):
    if RATE_LIMIT_ENABLED:

        checksum_response = to_checksum(duc_address)
        if checksum_response['status']:
            duc_address = checksum_response['address']
        else:
            return incorrect_address(checksum_response['error_message'])

        is_address_allowed = locking_check(DucatusAddress, duc_address)
        if not is_address_allowed:
            return duc_address_locked()

        is_ip_allowed = locking_check(IPAddress, ip)
        if not is_ip_allowed:
            return ip_address_locked()

        tx_response = make_tx(duc_address)
        if not tx_response['success']:
            return tx_failed(tx_response['error_message'])

        db_update(DucatusAddress, duc_address)
        db_update(IPAddress, ip)

        return success_response(duc_address)

@bot.message_handler()
def transaction_request(message):
    transaction_response = main_process(message.text, str(message.chat.id))
    bot.send_message(chat_id=message.chat.id, text=transaction_response.replace(',', '\n'))



if __name__ == '__main__':
    bot.polling()
