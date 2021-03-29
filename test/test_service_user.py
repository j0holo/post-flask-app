import pytest
from app.services import user as user_service
from app.postgres import user as user_postgres
from app.exceptions import PasswordsDoNotMatch, InvalidEmail
import psycopg2
from psycopg2 import DatabaseError, DataError


def test_create_user_passwords_do_not_match(conn):
    with pytest.raises(PasswordsDoNotMatch):
        user_service.create(conn, "x", "y", "z", "d", "")

def test_create_user(conn):
    username = "john"
    email = "john@example.com"
    password = "password"
    password_repeat = password
    profile_text = "lorem ipsum"

    try:
        user_service.create(conn, username, email, password, password_repeat, profile_text)
        conn.commit()
    except DataError as e:
        pytest.fail(e)
    except DatabaseError as e:
        pytest.fail(e)
    except PasswordsDoNotMatch as e:
        pytest.fail(e)

    u = user_postgres.get_by_email(conn, email)

    assert u.username == username
    assert u.email == email
    assert u.profile_text == profile_text

def test_email_is_valid():
    assert user_service.email_is_valid("john@example.com")

def test_email_is_invalid():
     assert not user_service.email_is_valid("john@example")
     assert not user_service.email_is_valid("johnexample.com")

def test_create_user_invalid_email(conn):
    invalid_email = "john@example"

    with pytest.raises(InvalidEmail):
        user_service.create(conn, "x", invalid_email, "x", "x", "")
