import pytest
import psycopg2


@pytest.fixture()
def connection():
    connection = psycopg2.connect("dbname=flask user=postgres password=password host=localhost")
    create_tables(connection)
    yield connection
    empty_tables(connection)
    connection.close()


def create_tables(connection):
    cursor = connection.cursor()
    with open("database.sql") as dbf:
        tables = dbf.read()
        cursor.execute(tables)
        connection.commit()
    cursor.close()


def empty_tables(connection):
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
    connection.commit()