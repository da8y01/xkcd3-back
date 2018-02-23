# coding: utf-8

from flask import url_for
from xkcd.exceptions import USER_NOT_FOUND


def _register_user(testapp, **kwargs):
    return testapp.post_json(url_for('users.register_user'), {
          "user": {
              "email": 'foo@bar.com',
              "first_name": 'foobar',
              "last_name": 'baz',
              "password": 'myprecious'
          }}, **kwargs)


class TestProfile:

    def test_get_profile_not_loggedin(self, testapp):
        _register_user(testapp)
        resp = testapp.get(url_for('profiles.get_profile', email='foo@bar.com'))
        assert resp.json['profile']['email'] == 'foo@bar.com'

    def test_get_profile_not_existing(self, testapp):
        resp = testapp.get(url_for('profiles.get_profile', email='foo@bar.com'), expect_errors=True)
        assert resp.status_int == 404
        assert resp.json == USER_NOT_FOUND['message']
