from app import db
from datetime import date


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(200))
    name = db.Column(db.String(64))
    email = db.Column(db.String(120))
    permission = db.Column(db.Integer)
    cargo = db.Column(db.String(120))
    data = db.Column(db.Date, default=date.today)
    is_online = db.Column(db.Boolean, default=False)
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.permission = permission
        self.cargo = cargo
        self.data = data

    def __repr__(self):
        return "<User %r>" % self.username


