from typing import List
from app.postgres import subscription


def subscribe(conn, user_id, author_id):
    subscription.subscribe(conn, user_id, author_id)

def unsibscribe(conn, user_id, author_id):
    subscription.unsubscribe(conn, user_id, author_id)

def get_authors_and_posts(conn, user_id) -> List[subscription.Subscription]:
    return subscription.get_authors_and_posts(conn, user_id)

def get_authors_and_posts(conn, user_id) -> List[str]:
    return subscription.get_authors_and_posts(conn, user_id)

