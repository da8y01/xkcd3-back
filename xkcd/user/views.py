# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_jwt import current_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from .models import User
from .serializers import user_schema
from xkcd.database import db
from xkcd.exceptions import InvalidUsage
from xkcd.extensions import cors
from xkcd.profile.models import UserProfile
from xkcd.utils import jwt_optional


blueprint = Blueprint('users', __name__)


@blueprint.route('/user', methods=('POST',))
@use_kwargs(user_schema)
@marshal_with(user_schema)
def register_user(first_name, last_name, password, email, **kwargs):
    try:
        userprofile = UserProfile(User(first_name, last_name, email, password=password, **kwargs).save()).save()
    except IntegrityError:
        db.session.rollback()
        raise InvalidUsage.user_already_registered()
    return userprofile.user


@blueprint.route('/user/login', methods=('POST',))
@jwt_optional()
@use_kwargs(user_schema)
@marshal_with(user_schema)
def login_user(email, password, **kwargs):
    user = User.query.filter_by(email=email).first()
    if user is not None and user.check_password(password):
        return user
    else:
        raise InvalidUsage.user_not_found()


@blueprint.route('/user', methods=('GET',))
@jwt_required()
@marshal_with(user_schema)
def get_user():
    return current_identity


@blueprint.route('/user', methods=('PUT',))
@jwt_required()
@use_kwargs(user_schema)
@marshal_with(user_schema)
def update_user(**kwargs):
    user = current_identity
    # take in consideration the password
    password = kwargs.pop('password', None)
    if password:
        user.set_password(password)
    user.update(**kwargs)
    return user
