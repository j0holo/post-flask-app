from flask import Blueprint, current_app, request, jsonify
from app.services import post
import psycopg2
import logging


post_blueprint = Blueprint('post_blueprint', __name__)

@post_blueprint.route('/posts/', methods=['GET'])
def by_author():
    conn = psycopg2.connect(current_app.config['DSN'])

    author = request.args.get('author')
    # TODO: Catch exceptions and return a appropriate response.
    try:
        posts = post.get_posts_by_author(conn, author)
    except Exception as e:
        logging.info(e)
        # return catch_exception(e).error

    return jsonify(posts)