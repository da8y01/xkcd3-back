# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from xkcd.user.models import User
from xkcd.profile.models import UserProfile
from xkcd.comics.models import Comic


from .factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""

    def test_get_by_id(self):
        """Get user by ID."""
        user = User('foo', 'bar', 'foo@bar.com', '12345678')
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory(password='myprecious')
        db.session.commit()
        assert bool(user.first_name)
        assert bool(user.last_name)
        assert bool(user.email)
        assert user.check_password('myprecious')

    def test_check_password(self):
        """Check password."""
        user = User.create(first_name='foo', last_name='bar', email='foo@bar.com',
                           password='foobarbaz123')
        assert user.check_password('foobarbaz123')
        assert not user.check_password('barfoobaz')


@pytest.mark.usefixtures('db')
class TestComics:
    def test_create_comic(self, user):
        u1 = user.get()
        comic = Comic(u1.profile, "1", "314", "http://comic.com", "2001", "the news", "the safe title", "the transcript", "the alt", "http://comic.png", "the title", "1")
        comic.save()
        assert comic.author.user == u1
