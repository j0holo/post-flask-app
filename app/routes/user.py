from flask import Blueprint, current_app, request
from app.services import user
import psycopg2
import logging

user_blueprint = Blueprint('user_blueprint', __name__)

# POST /users/


@user_blueprint.route('/', methods=['POST'])
def create():
    conn = psycopg2.connect(current_app.config['DSN'])

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password_repeat = request.form['password_repeat']
    profile_text = request.form['profile_text']

    # TODO: Catch exceptions and return a appropriate response.
    try:
        user.create(conn, username, email, password,
                    password_repeat, profile_text)
    except Exception as e:
        logging.info(e)
        return catch_exception(e).error

    # TODO: Replace this with the real message
    return success_response_message
