# ----------------------------------------------------
# Program by Andrey Vestimy
#
#
# Version   Date    Info
# 1.0       2020    ----
#
# ----------------------------------------------------

from classDb import db, session, Base
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
import uuid



class Users(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    login = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    tokens_id = relationship('Tokens', backref='users', lazy=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.login = kwargs.get('login')
        self.password = bcrypt.hash(kwargs.get('password'))

    @classmethod
    def authentificate(cls, login, password):
        try:
            user = cls.query.filter(cls.login == login).one()
            if not bcrypt.verify(password, user.password):
                return False
        except:
            return False
        return user

class Tokens(Base):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__(self, id):
        self.token = uuid.uuid4().hex
        self.user_id = id
