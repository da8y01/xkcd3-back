# coding: utf-8

from flask import url_for
from datetime import datetime

class TestComicViews:

    def test_get_comics_by_author(self, testapp, user):
        user = user.get()
        resp = testapp.post_json(url_for('users.login_user'), {'user': {
            'email': user.email,
            'password': 'myprecious'
        }})

        token = str(resp.json['user']['token'])
        for _ in range(2):
            testapp.post_json(url_for('comics.make_comic'), {
                "comic": {
                    "month": "{}".format(_),
                    "num": "{}".format(_),
                    "link": "http://comic.com",
                    "year": "2001",
                    "news": "the news",
                    "safe_title": "the safe title",
                    "transcript": "the transcript",
                    "alt": "the alt",
                    "img": "http://comic.png",
                    "title": "the title",
                    "day": "1"
                }
            }, headers={
                'Authorization': 'Token {}'.format(token)
            })

        resp = testapp.get(url_for('comics.get_comics', author=user.email))
        assert len(resp.json['comics']) == 2

    def test_make_comic(self, testapp, user):
        user = user.get()
        resp = testapp.post_json(url_for('users.login_user'), {'user': {
            'email': user.email,
            'password': 'myprecious'
        }})

        token = str(resp.json['user']['token'])
        resp = testapp.post_json(url_for('comics.make_comic'), {
            "comic": {
                "month": "1",
                "num": "314",
                "link": "http://comic.com",
                "year": "2001",
                "news": "the news",
                "safe_title": "the safe title",
                "transcript": "the transcript",
                "alt": "the alt",
                "img": "http://comic.png",
                "title": "the title",
                "day": "1"
            }
        }, headers={
            'Authorization': 'Token {}'.format(token)
        })
        assert resp.json['comic']['author']['email'] == user.email
        assert resp.json['comic']['title'] == 'the title'
