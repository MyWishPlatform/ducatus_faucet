from app import app
from flask import request
from app.models import DucatusAddress, IPAddress
from app.queries import check_and_update, db_update, make_tx
from app.responses import duc_address_locked, ip_address_locked, tx_failed, success_response
from settings_local import RATELIMIT_ENABLED


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/request/', methods=['POST'])
def transaction_request():
    if RATELIMIT_ENABLED:
        duc_address = request.get_json()['address']
        print(duc_address)

        is_address_allowed = check_and_update(DucatusAddress, duc_address)
        if not is_address_allowed:
            return duc_address_locked()

        ip = request.headers.getlist("X-Forwarded-For")[0] if request.headers.getlist(
            "X-Forwarded-For") else request.remote_addr

        is_ip_allowed = check_and_update(IPAddress, ip)
        if not is_ip_allowed:
            return ip_address_locked()

        tx_response = make_tx(duc_address)
        if not tx_response['success']:
            return tx_failed(tx_response['error_message'])

        db_update(DucatusAddress, duc_address)
        db_update(IPAddress, ip)

        return success_response(duc_address)

