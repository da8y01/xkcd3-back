# -*- coding: utf-8 -*-
"""User models."""
import datetime

from flask_jwt import _default_jwt_encode_handler

from xkcd.database import Column, Model, SurrogatePK, db
from xkcd.extensions import bcrypt

from bson import ObjectId


class User(SurrogatePK, Model):

    __tablename__ = 'users'
    id = Column(db.String(30), primary_key=True, unique=True, nullable=False)
    first_name = Column(db.String(80), unique=False, nullable=False)
    last_name = Column(db.String(80), unique=False, nullable=False)
    email = Column(db.String(100), unique=True, nullable=False)
    password = Column(db.Binary(128), nullable=False)

    def __init__(self, first_name, last_name, email, password, **kwargs):
        """Create instance."""
        dummy_id = str(ObjectId.from_datetime(datetime.datetime.now()))
        db.Model.__init__(self, id=dummy_id, first_name=first_name, last_name=last_name, email=email, password=password, **kwargs)
        self.set_password(password)

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def token(self):
        return _default_jwt_encode_handler(self).decode('utf-8')

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({email!r})>'.format(email=self.email)
