from psycopg2.extras import DictCursor
from psycopg2.extensions import connection
from app.exceptions import PostNotFoundError
from app.postgres.post import Post
from slugify import slugify


def generate_slug(title: str) -> str:
    return slugify(title)


def create(conn: connection, author: int, title: str, content: str):
    with conn.cursor() as cursor:
        query = """
            INSERT INTO posts (title, slug, author, content)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (title, generate_slug(title), author, content))


def update(conn: connection, post_id: int, title: str, content: str):
    with conn.cursor() as cursor:
        query = "UPDATE posts SET title=%s, content=%s WHERE id=%s"
        cursor.execute(query, (title, content, post_id))


def get_post_by_slug(conn: connection, username: str, slug: str):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        query = """
            SELECT posts.id, posts.title, posts.slug,
            posts.posted_at, posts.updated_at, posts.content, users.username author
            FROM posts
            JOIN users ON users.id = posts.author
            WHERE slug=%s AND users.username=%s
        """
        curs.execute(query, (slug, username))
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
