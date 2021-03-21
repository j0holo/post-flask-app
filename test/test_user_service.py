import app.user
import pytest
from app import user
from app.exceptions import UserNotFoundError
import psycopg2
from psycopg2 import DatabaseError, DataError


def test_get_user_by_email(connection):
    email = "john@example.com"

    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (email) VALUES (%s)", (email,))
        connection.commit()
        cursor.close()
    except DataError as e:
        pytest.fail(e)
    except DatabaseError as e:
        pytest.fail(e)

    u = user.get_by_email(connection, email)

    assert u.email == email

def test_get_nonexisting_user_by_email(connection):
    email = "john@example.com"

    with pytest.raises(UserNotFoundError):
        user.get_by_email(connection, email)
