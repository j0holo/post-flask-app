import app.user
import pytest
from app import user
from app.exceptions import UserNotFoundError
import psycopg2
from psycopg2 import DatabaseError, DataError

# Given that the email is valid, username is valid and the email is not taken by another user and the password is strong enough
# When the user creates a new account
# Then the user receives an Okay response
# And an activation email is send

@pytest.fixture()
def conn():
    conn = psycopg2.connect("user=postgres password=password host=localhost")
    create_tables(conn)
    yield conn
    empty_tables(conn)
    conn.close()

def create_tables(conn):
    cursor = conn.cursor()
    with open("database.sql") as dbf:
        tables = dbf.read()
        cursor.execute(tables)
        conn.commit()
    cursor.close()

def empty_tables(conn):
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
    conn.commit()

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
