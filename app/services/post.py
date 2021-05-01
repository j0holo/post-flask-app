from psycopg2.extras import DictCursor
from psycopg2.extensions import connection
from app.exceptions import PostNotFoundError
from app.postgres.post import Post


def generate_slug(title: str) -> str:
    return title.replace(" ", "-").lower()


def create_post(conn: connection, author: int, title: str, content: str):
    with conn.cursor() as cursor:
        query = """
            INSERT INTO posts (title, slug, author, content)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (title, generate_slug(title), author, content))
    

def update_post(conn: connection, post_id: int, title: str, content: str):
    with conn.cursor() as cursor:
        query = "UPDATE posts SET title=%s, content=%s WHERE id=%s"
        cursor.execute(query, (title, content, post_id))


def get_post_by_slug(conn: connection, slug: str, author: int):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        query = """
            SELECT id, title, slug, author, posted_at, updated_at, content\
            FROM posts
            WHERE slug=%s AND author=%s
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