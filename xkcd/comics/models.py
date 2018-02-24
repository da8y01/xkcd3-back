# coding: utf-8

import datetime

from flask_jwt import current_identity
from slugify import slugify

from xkcd.database import (Model, SurrogatePK, db, Column,
                              reference_col, relationship)
from xkcd.profile.models import UserProfile

from bson import ObjectId


class Comic(SurrogatePK, Model):
    __tablename__ = 'comic'

    id = db.Column(db.String(30), primary_key=True)
    month = Column(db.String(2), nullable=False)
    num = Column(db.Integer, unique=True, nullable=False)
    link = Column(db.String(100), nullable=False)
    year = Column(db.String(4), nullable=False)
    news = Column(db.Text, nullable=False)
    safe_title = Column(db.Text, nullable=False)
    transcript = Column(db.Text, nullable=False)
    alt = Column(db.Text, nullable=False)
    img = Column(db.String(200), nullable=False)
    title = Column(db.String(100), nullable=False)
    day = Column(db.String(2), nullable=False)
    author_id = reference_col('userprofile', nullable=True)
    author = relationship('UserProfile', backref=db.backref('comics'))

    def __init__(self, author, month, num, link, year,
                          news, safe_title, transcript, alt, 
                          img, title, day, **kwargs):
        dummy_id = str(ObjectId.from_datetime(datetime.datetime.now()))
        db.Model.__init__(self, id=dummy_id, month=month, num=num, link=link, year=year,
                          news=news, safe_title=safe_title, transcript=transcript, alt=alt, 
                          img=img, title=title, day=day, **kwargs)
