import json


def response_callback(error_type, msg):
    payload = {
        'success': False,
        'code': error_type,
        'msg': msg
    }

    return json.dumps(payload)


def ip_address_locked():
    return response_callback(601, "IP limit: 1 request per day")


def duc_address_locked():
    return response_callback(602, "Address limit: 1 address per day")


def tx_failed(err):
    return response_callback(603, err)


def incorrect_address(err):
    return response_callback(604, err)


def success_response(address):
    return json.dumps({'success': True, 'code': 200, 'msg': address})
