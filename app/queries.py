import datetime
from app import db
from settings_local import *
from web3 import Web3, HTTPProvider


def to_checksum(address):
    try:
        address = Web3.toChecksumAddress(address)
        return {'status': True, 'address': address}
    except ValueError as error:
        return {'status': False, 'error_message': str(error)}


def locking_check(model, address):
    db_address = model.query.filter_by(address=address).first()
    if db_address:
        if db_address.last_transaction_date <= datetime.datetime.now() - datetime.timedelta(**blocking_time):
            return True
    else:
        return True


def db_update(model, address):
    user_info = model.query.filter_by(address=address).first()
    if user_info:
        user_info.last_transaction_date = datetime.datetime.now()
        db.session.commit()
    else:
        user_info = model(address=address, last_transaction_date=datetime.datetime.now())
        db.session.add(user_info)
        db.session.commit()


def make_tx(address):
    try:
        w3 = Web3(HTTPProvider('http://{host}:{port}'.format(host=duc_host, port=duc_port)))

        tx = {
            'nonce': w3.eth.getTransactionCount(duc_address, 'pending'),
            'gasPrice': w3.eth.gasPrice,
            'gas': gas_value,
            'to': address,
            'value': DROP_AMOUNT,
            'data': b'',
            'chainId': w3.eth.chainId,
            'from': duc_address
        }

        signed_txn = w3.eth.account.signTransaction(tx, private_key)

        w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return {'success': True}
    except Exception as error:
        return {'success': False, 'error_message': str(error)}
