from app.exceptions import UserNotFoundError
from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    email: str
    profile_text: str

def get_by_email(conn, email):
    with conn.cursor() as curs:
        curs.execute("SELECT id, username, email, profile_text FROM users WHERE email = %s", (email,))
        row = curs.fetchone()

    if row is None:
        raise UserNotFoundError
    return User(row[0], row[1], row[2], row[3])


def create():
    pass