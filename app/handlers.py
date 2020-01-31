from app import app
from flask import request
from app.queries import main_process
from settings_local import RATE_LIMIT_ENABLED
from flask import make_response


@app.route('/api/request/', methods=['POST'])
def transaction_request():
    if RATE_LIMIT_ENABLED:
        duc_address = request.get_json()['address']

        ip = request.headers.getlist("X-Forwarded-For")[0] if request.headers.getlist(
            "X-Forwarded-For") else request.remote_addr

        return make_response(main_process(duc_address, ip))


