from psycopg2.extras import DictCursor
from psycopg2.extensions import connection
from app.exceptions import PostNotFoundError
from app.postgres.post import Post


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