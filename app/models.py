from app import db


class DucatusAddress(db.Model):
    __tablename__ = 'ducatus_address'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(64), index=True, unique=True, nullable=False)
    last_transaction_date = db.Column(db.DateTime(timezone=False), nullable=False)


class IPAddress(db.Model):
    __tablename__ = 'ip_address'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(40), index=True, unique=True, nullable=False)
    last_transaction_date = db.Column(db.DateTime(timezone=False), nullable=False)
