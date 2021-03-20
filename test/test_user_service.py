import app.user
import pytest

# Given that the email is valid, username is valid and the email is not taken by another user and the password is strong enough
# When the user creates a new account
# Then the user receives an Okay response
# And an activation email is send


def test_get_user():
    # TODO: setup database

    email = "john@example.com"
    user = user.get_by_email(email)

    assert user.email == email