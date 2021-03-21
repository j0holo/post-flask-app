from psycopg2.extras import DictCursor
from psycopg2.extensions import connection
from .exceptions import PostNotFoundError
from dataclasses import dataclass
from time import time


@dataclass
class Post:
    id: int
    title: str
    slug: str
    author: int
    posted_at: time
    updated_at: time
    content: str


def get_post_by_slug(connection: connection, slug: str, author: int):
    with connection.cursor(cursor_factory=DictCursor) as curs:
        query = """\
            SELECT id, title, slug, author, posted_at, updated_at, content\
            FROM posts\
            WHERE slug=%s AND author=%s\
        """
        curs.execute(query, (slug, author))
        row = curs.fetchone()

    if row is None:
        raise PostNotFoundError
    return Post(
        row['id'], 
        row['title'], 
        row['slug'], 
        row['author'], 
        row['posted_at'], 
        row['updated_at'], 
        row['content']
    )