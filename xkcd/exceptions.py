from flask import jsonify


def template(data, code=500):
    return {'message': {'message': data, 'status': code}, 'status_code': code}


USER_NOT_FOUND = template('User not found', code=404)
USER_BAD_CREDENTIALS = template('Please check your credentials', code=401)
USER_ALREADY_EXISTS = template('User with that email already exists', code=400)
USER_ALREADY_REGISTERED = template('User already registered', code=422)
UKNOWN_ERROR = template('Server error', code=500)
COMIC_NOT_FOUND = template('Comic not found', code=404)


class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.message
        return jsonify(rv)

    @classmethod
    def user_not_found(cls):
        return cls(**USER_NOT_FOUND)

    @classmethod
    def user_already_registered(cls):
        return cls(**USER_ALREADY_REGISTERED)

    @classmethod
    def user_already_exists(cls):
        return cls(**USER_ALREADY_EXISTS)

    @classmethod
    def user_bad_credentials(cls):
        return cls(**USER_BAD_CREDENTIALS)

    @classmethod
    def uknown_error(cls):
        return cls(**UKNOWN_ERROR)

    @classmethod
    def comic_not_found(cls):
        return cls(**COMIC_NOT_FOUND)
