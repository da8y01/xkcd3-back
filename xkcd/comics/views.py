# coding: utf-8

import time

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
@use_kwargs({'limit': fields.Int(), 'offset': fields.Int()})
@marshal_with(comics_schema)
def get_comics(limit=20, offset=0):
    res = Comic.query
    #return res.offset(offset).limit(limit).all()
    return res.all()


@blueprint.route('/comic', methods=('POST',))
@jwt_required()
@use_kwargs(comic_schema)
@marshal_with(comic_schema)
def make_comic(month, num, link, year, news, safe_title, transcript, alt, img, title, day, id=None):
    comic = None
    if type(id) == unicode:
        comic = Comic.query.filter_by(num=num).first()
        if not comic:
            raise InvalidUsage.comic_not_found()
        else:
            comic.update(month=month, link=link, year=year, news=news, safe_title=safe_title, transcript=transcript, alt=alt, img=img, title=title, day=day)
    else:
        comic = Comic(month=month, num=num, link=link, year=year, news=news, safe_title=safe_title, transcript=transcript, alt=alt, img=img, title=title, day=day)
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
    comic.save()
    return comic


@blueprint.route('/comic/<slug>', methods=('DELETE',))
@jwt_required()
def delete_comic(slug):
    comic = Comic.query.filter_by(slug=slug, author_id=current_identity.profile.id).first()
    comic.delete()
    return '', 200


@blueprint.route('/comic/<num>', methods=('GET',))
@jwt_optional()
@marshal_with(comic_schema)
def get_comic(num):
    comic = Comic.query.filter_by(num=num).first()
    if not comic:
        raise InvalidUsage.comic_not_found()
    return comic
