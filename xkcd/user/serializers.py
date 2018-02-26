# coding: utf-8

from marshmallow import Schema, fields, pre_load, post_dump


class UserSchema(Schema):
    id = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    password = fields.Str(load_only=True)
    token = fields.Str(dump_only=True)
    # ugly hack.
    user = fields.Nested('self', exclude=('user',), default=True, load_only=True)

    @pre_load
    def make_user(self, data):
        # some of the frontends send this like an empty string and some send
        # null
        if not data.get('email', True):
            del data['email']
        return data

    @post_dump
    def dump_user(self, data):
        return {'status':'200', 'message':'The user was created successfully', 'id':data['id'], 'user':data}

    class Meta:
        strict = True


user_schema = UserSchema()
user_schemas = UserSchema(many=True)
