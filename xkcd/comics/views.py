# coding: utf-8

import datetime as dt

from flask import Blueprint, jsonify
from flask_apispec import marshal_with, use_kwargs
from flask_jwt import jwt_required, current_identity
from marshmallow import fields

from .models import Comic
from .serializers import (comic_schema, comics_schema)
from xkcd.exceptions import InvalidUsage
from xkcd.extensions import cors
from xkcd.user.models import User
from xkcd.utils import jwt_optional


blueprint = Blueprint('comics', __name__)


##########
# Comics
##########

@blueprint.route('/comic', methods=('GET',))
@jwt_optional()
@use_kwargs({'author': fields.Str(), 'limit': fields.Int(), 'offset': fields.Int()})
@marshal_with(comics_schema)
def get_comics(author=None, limit=20, offset=0):
    res = Comic.query
    if author:
        res = res.join(Comic.author).join(User).filter(User.email == author)
    return res.offset(offset).limit(limit).all()


@blueprint.route('/comic', methods=('POST',))
@jwt_required()
@use_kwargs(comic_schema)
@marshal_with(comic_schema)
def make_comic(month, num, link, year, news, safe_title, transcript, alt, img, title, day):
    comic = Comic(month=month, num=num, link=link, year=year, news=news, safe_title=safe_title, transcript=transcript, alt=alt, img=img, title=title, day=day,
                      author=current_identity.profile)
    comic.save()
    return comic


@blueprint.route('/comic/<slug>', methods=('PUT',))
@jwt_required()
@use_kwargs(comic_schema)
@marshal_with(comic_schema)
def update_comic(slug, **kwargs):
    comic = Comic.query.filter_by(slug=slug, author_id=current_identity.profile.id).first()
    if not comic:
        raise InvalidUsage.comic_not_found()
    comic.update(updatedAt=dt.datetime.utcnow, **kwargs)
    comic.save()
    return comic


@blueprint.route('/comic/<slug>', methods=('DELETE',))
@jwt_required()
def delete_comic(slug):
    comic = Comic.query.filter_by(slug=slug, author_id=current_identity.profile.id).first()
    comic.delete()
    return '', 200


@blueprint.route('/comic/<slug>', methods=('GET',))
@jwt_optional()
@marshal_with(comic_schema)
def get_comic(slug):
    comic = Comic.query.filter_by(slug=slug).first()
    if not comic:
        raise InvalidUsage.comic_not_found()
    return comic


@blueprint.route('/comic/feed', methods=('GET',))
@jwt_required()
@use_kwargs({'limit': fields.Int(), 'offset': fields.Int()})
@marshal_with(comics_schema)
def comics_feed(limit=20, offset=0):
    return Comics.query.join(current_identity.profile.follows).\
        order_by(Comic.createdAt.desc()).offset(offset).limit(limit).all()
