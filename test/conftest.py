import pytest
import psycopg2


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
