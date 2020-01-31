from app import app
from flask import request
from app.models import DucatusAddress, IPAddress
from app.queries import locking_check, db_update, make_tx, to_checksum
from app.responses import duc_address_locked, ip_address_locked, tx_failed, incorrect_address, success_response
from settings_local import RATE_LIMIT_ENABLED


@app.route('/api/request/', methods=['POST'])
def transaction_request():
    if RATE_LIMIT_ENABLED:
        duc_address = request.get_json()['address']

        checksum_response = to_checksum(duc_address)
        if checksum_response['status']:
            duc_address = checksum_response['address']
        else:
            return incorrect_address(checksum_response['error_message'])

        print(duc_address)

        is_address_allowed = locking_check(DucatusAddress, duc_address)
        if not is_address_allowed:
            return duc_address_locked()

        ip = request.headers.getlist("X-Forwarded-For")[0] if request.headers.getlist(
            "X-Forwarded-For") else request.remote_addr

        is_ip_allowed = locking_check(IPAddress, ip)
        if not is_ip_allowed:
            return ip_address_locked()

        tx_response = make_tx(duc_address)
        if not tx_response['success']:
            return tx_failed(tx_response['error_message'])

        db_update(DucatusAddress, duc_address)
        db_update(IPAddress, ip)

        return success_response(duc_address)
