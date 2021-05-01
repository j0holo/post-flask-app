import pytest
from app.services.post import get_post_by_slug
from psycopg2 import DatabaseError, DataError

# /<username>/posts/<slug>/
# /<username>/posts/

def test_get_post_by_slug(conn):
    title = "How create a programing language"
    slug = "how-create-a-programming-language"
    username = 'testuser'
    author = 1
    content = "BLA BLA BLA"

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username) VALUES (%s)", (username, ))
        conn.commit()
        query = """\
            INSERT INTO posts (title, slug, author, content)\
            VALUES (%s, %s, %s, %s)\
        """
        cursor.execute(query, (title, slug, author, content))
        conn.commit()
        cursor.close()
    except (DataError, DatabaseError) as e:
        pytest.fail(e)
        
    post = get_post_by_slug(conn, slug, author)
    assert post.slug == slug
    assert post.author == author
    assert post.content == content
    assert post.title == title
