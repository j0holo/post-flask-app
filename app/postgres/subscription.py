from psycopg2.extras import DictCursor
from dataclasses import dataclass
from app.postgres.post import Post
from typing import List

@dataclass
class Subscription:
    author: str
    posts: List[Post]


def subscribe(conn, user_id, author_id):
    with conn.cursor() as curs:
        curs.execute("INSERT INTO subscriptions (user_id, author) VALUES (%s, %s)", (user_id, author_id))

def unsubscribe(conn, user_id, author_id):
    with conn.cursor() as curs:
        curs.execute("DELETE FROM subscriptions WHERE user_id = %s AND author = %s", (user_id, author_id))

def get_authors_and_posts(conn, user_id) -> List[Subscription]:
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute("""SELECT u.username AS username, p.id AS post_id, title, slug, posted_at, updated_at FROM subscriptions AS s
        INNER JOIN users AS u ON u.id = s.author
        INNER JOIN posts AS p ON p.author = s.author
        WHERE s.user_id = %s
        ORDER BY posted_at ASC""", (user_id,))

        rows = curs.fetchall()

        subscriptions = list()

        sub  = Subscription("", [])

        for row in rows:
            if sub.author != "" and sub.author != row['username']:
                subscriptions.append(sub)
                sub = Subscription("", [])

            sub.author = row['username']
            sub.posts.append(Post(
                id=row["post_id"],
                title=row['title'],
                slug=row['slug'],
                author=row['username'],
                posted_at=row['posted_at'],
                updated_at=row['updated_at'],
                content=""
            ))

    return subscriptions

def get_authors(conn, user_id) -> List[str]:
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute("""SELECT u.username AS username
        FROM subscriptions AS s
        INNER JOIN users AS u ON u.id = s.author
        WHERE s.user_id = %s
        ORDER BY username ASC""", (user_id,))

        rows = curs.fetchall()

        authors = list()

        for row in rows:
            authors.append(row[0])

    return authors
