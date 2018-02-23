# coding: utf-8

from flask import Blueprint
from flask_apispec import marshal_with
from flask_jwt import current_identity, jwt_required

from .serializers import profile_schema
from xkcd.exceptions import InvalidUsage
from xkcd.extensions import cors
from xkcd.user.models import User
from xkcd.utils import jwt_optional


blueprint = Blueprint('profiles', __name__)


@blueprint.route('/profiles/<email>', methods=('GET',))
@jwt_optional()
@marshal_with(profile_schema)
def get_profile(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        raise InvalidUsage.user_not_found()
    return user.profile
