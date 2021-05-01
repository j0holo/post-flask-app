import pytest
from app.services.post import (
    get_post_by_slug, 
    create_post, 
    update_post
)
from app.services.user import create
from psycopg2 import DatabaseError, DataError

# /<username>/posts/<slug>/
# /<username>/posts/

def test_get_post_by_slug(conn):
    title = "How create a programing language"
    slug = "how-create-a-programming-language"
    username = 'testuser'
    author = 1
    content = "BLA BLA BLA"

    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (username) VALUES (%s)", (username, ))
            conn.commit()
            query = """\
                INSERT INTO posts (title, slug, author, content)\
                VALUES (%s, %s, %s, %s)\
            """
            cursor.execute(query, (title, slug, author, content))
    except (DataError, DatabaseError) as e:
        pytest.fail(e)
        
    post = get_post_by_slug(conn, slug, author)
    assert post.slug == slug
    assert post.author == author
    assert post.content == content
    assert post.title == title


def test_create_post(conn):
    author = 1
    title = "Pytest test"
    slug = "pytest-test"
    content = "foo"
    create(conn, "username", "username@gmail.com", "123456", "123456", "profile")
    create_post(conn, author, title, content)
    post = get_post_by_slug(conn, slug, author)
    assert post.title == title
    assert post.slug == slug
    assert post.author == author
    assert post.content == content

def test_update_post(conn):
    author = 1
    old_title = "Pytest test"
    old_slug = "pytest-test"
    old_content = "foo"
    new_title = "Pytest test 2"
    new_slug = "pytest-test-2"
    new_content = "bar"

    create(conn, "username", "username@gmail.com", "123456", "123456", "profile")
    create_post(conn, author, old_title, old_content)
    old_post = get_post_by_slug(conn, old_slug, author)
    
    create_post(conn, author, new_title, new_content)
    new_post = get_post_by_slug(conn, new_slug, author)
    
    assert not new_post.content == old_post.content
    assert not new_post.title == old_post.title
    assert not new_post.content == old_post.content