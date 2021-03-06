# coding: utf-8

from marshmallow import Schema, fields, pre_load, post_dump

from xkcd.profile.serializers import ProfileSchema


class ComicSchema(Schema):
    id = fields.Str(partial=True)
    month = fields.Str()
    num = fields.Int()
    link = fields.Str()
    year = fields.Str()
    news = fields.Str()
    safe_title = fields.Str()
    transcript = fields.Str()
    alt = fields.Str()
    img = fields.Str()
    title = fields.Str()
    day = fields.Str()
    comic = fields.Nested('self', exclude=('comic',), default=True, load_only=True)

    @pre_load
    def make_comic(self, data):
        return data

    @post_dump
    def dump_comic(self, data):
        return data

    class Meta:
        strict = True


class ComicSchemas(ComicSchema):

    @post_dump
    def dump_comic(self, data):
        return data

    @post_dump(pass_many=True)
    def dump_comics(self, data, many):
        return {'comics': data, 'comicsCount': len(data)}


comic_schema = ComicSchema()
comics_schema = ComicSchemas(many=True)
