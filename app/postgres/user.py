from app.exceptions import UserNotFoundError, IncorrectPassword
from dataclasses import dataclass
import bcrypt

BCRYPT_ROUNDS = 12

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


def create(conn, username, email, password, profile_text):
    hash = hash_password(conn, password).decode('utf8')
    with conn.cursor() as curs:
        curs.execute("INSERT INTO users (username, email, password, profile_text) VALUES (%s, %s, %s, %s)", (username, email, hash, profile_text))

def check_password(conn, email, password) -> bool:
    with conn.cursor() as curs:
        curs.execute("SELECT password FROM users WHERE email = %s", (email,))
        row = curs.fetchone()

    if row is None:
        raise UserNotFoundError

    hash = row[0].encode('utf8')
    return bcrypt.checkpw(password.encode('utf8'), hash)

def hash_password(conn, password) -> str:
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(BCRYPT_ROUNDS))
