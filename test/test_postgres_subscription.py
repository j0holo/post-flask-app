import pytest
from app.postgres import subscription, user
from app.services import post as post_service
from psycopg2 import DatabaseError, DataError


def test_subscribe_to_author(conn):
    email1 = "john@example.com"
    email2 = "karen@example.com"

    try:
        user.create(conn, email1, email1, "password", "")
        user.create(conn, email2, email2, "password", "")

        user1 = user.get_by_email(conn, email1)
        user2 = user.get_by_email(conn, email2)

        conn.commit()
    except DataError as e:
        pytest.fail(e)
    except DatabaseError as e:
        pytest.fail(e)

    subscription.subscribe(conn, user1.id, user2.id)

def test_unsubscribe(conn):
    email1 = "john@example.com"
    email2 = "karen@example.com"

    try:
        user.create(conn, email1, email1, "password", "")
        user.create(conn, email2, email2, "password", "")

        user1 = user.get_by_email(conn, email1)
        user2 = user.get_by_email(conn, email2)
        subscription.subscribe(conn, user1.id, user2.id)
        conn.commit()
    except DataError as e:
        pytest.fail(e)
    except DatabaseError as e:
        pytest.fail(e)

    subscription.unsubscribe(conn, user1.id, user2.id)

def test_get_authors_and_posts(conn):
    user1 = user.User(0, "user1", "john@example.com", "")
    user2 = user.User(0, "user2", "karen@example.com", "")

    try:
        user.create(conn, user1.username, user1.email, "password", "")
        user.create(conn, user2.username, user2.email, "password", "")

        user1 = user.get_by_email(conn, user1.email)
        user2 = user.get_by_email(conn, user2.email)

        post_service.create(conn, user2.id, "first post", "content")
        post_service.create(conn, user2.id, "second post", "content")

        subscription.subscribe(conn, user1.id, user2.id)
        conn.commit()

        subscriptions = subscription.get_authors_and_posts(conn, user1.id)
    except DataError as e:
        pytest.fail(e)
    except DatabaseError as e:
        pytest.fail(e)

    for sub in subscriptions:
        assert sub.author == user2.username
        for p in sub.posts:
            assert p.author == user2.username
            assert p.title in ["first post", "second post"]
            assert p.content == "content"

def test_get_authors(conn):
    user1 = user.User(0, "user1", "john@example.com", "")
    user2 = user.User(0, "user2", "karen@example.com", "")
    user3 = user.User(0, "user3", "dan@example.com", "")

    try:
        user.create(conn, user1.username, user1.email, "password", "")
        user.create(conn, user2.username, user2.email, "password", "")
        user.create(conn, user3.username, user3.email, "password", "")

        user1 = user.get_by_email(conn, user1.email)
        user2 = user.get_by_email(conn, user2.email)
        user3 = user.get_by_email(conn, user3.email)

        subscription.subscribe(conn, user1.id, user2.id)
        subscription.subscribe(conn, user1.id, user3.id)
        conn.commit()

        authors = subscription.get_authors(conn, user1.id)
    except DataError as e:
        pytest.fail(e)
    except DatabaseError as e:
        pytest.fail(e)

    assert "user2" in authors
    assert "user3" in authors
    assert "user1" not in authors
