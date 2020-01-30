from settings_local import *


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTGRES = {
        'user': db_user,
        'pw': db_password,
        'db': db_name,
        'host': db_host,
        'port': db_port,
    }

    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
