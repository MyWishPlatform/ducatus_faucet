import datetime
from app import db
from settings_local import *
from web3 import Web3, HTTPProvider, IPCProvider


def check_and_update(model, address):
    db_address = model.query.filter_by(address=address).first()
    if db_address:
        print(db_address.__dict__)
        if db_address.last_transaction_date <= datetime.datetime.now() - datetime.timedelta(minutes=5):
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
    return True

def sign_tx(address):
    w3 = Web3(HTTPProvider('http://{host}:{port}'.format(host=duc_host, port=duc_port)))

    signed_txn = w3.eth.account.signTransaction({
        'nonce': w3.eth.getTransactionCount(w3.eth.coinbase),
        'gasPrice': w3.eth.gasPrice,
        'gas': 100000,
        'to': address,
        'value': DROP_AMOUNT,
        'data': b''
    }, key)

    w3.eth.sendRawTransaction(signed_txn.rawTransaction)

