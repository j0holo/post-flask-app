import pytest
from app.postgres import user
from app.exceptions import UserNotFoundError
import psycopg2
from psycopg2 import DatabaseError, DataError

def test_get_user_by_email(conn):
    email = "john@example.com"

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email) VALUES (%s)", (email,))
        conn.commit()
        cursor.close()
    except DataError as e:
        pytest.fail(e)
    except DatabaseError as e:
        pytest.fail(e)

    u = user.get_by_email(conn, email)

    assert u.email == email

def test_get_nonexisting_user_by_email(conn):
    email = "john@example.com"

    with pytest.raises(UserNotFoundError):
        user.get_by_email(conn, email)


def test_create_new_account(conn):
    username = "john"
    email = "john@example.com"
    password = "password"
    profile_text = "lorem ipsum"

    cursor = conn.cursor()
    try:
        user.create(conn, username, email, password, profile_text)
        conn.commit()
        cursor.close()
    except DataError as e:
        pytest.fail(e)
    except DatabaseError as e:
        pytest.fail(e)

    u = user.get_by_email(conn, email)

    assert u.username == username
    assert u.email == email
    assert u.profile_text == profile_text

def test_create_new_account_and_password_is_encrypted(conn):
    username = "john"
    email = "john@example.com"
    password = "password"
    profile_text = "lorem ipsum"

    cursor = conn.cursor()
    try:
        user.create(conn, username, email, password, profile_text)
        conn.commit()
        cursor.close()
    except DataError as e:
        pytest.fail(e)
    except DatabaseError as e:
        pytest.fail(e)

    assert user.check_password(conn, email, password)
