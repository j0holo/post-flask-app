from app.exceptions import PasswordsDoNotMatch, InvalidEmail
from app.postgres import user
import re

email_regex = re.compile(r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')

def create(conn, username, email, password, password_repeat, profile_text):
    if password != password_repeat:
        raise PasswordsDoNotMatch
    if not email_is_valid(email):
        raise InvalidEmail
    user.create(conn, username, email, password, profile_text)

def email_is_valid(email) -> bool:
    return email_regex.search(email)

def update_password(conn, email, new_password):
    user.update_password(conn, email, new_password)


def get_profile(conn, username) -> user.User:
    return user.get_by_username(conn, username)
