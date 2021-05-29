import pytest
from app.services import post as post_service, user
from psycopg2 import DatabaseError, DataError
from psycopg2.extras import DictCursor


def test_get_post_by_slug(conn):
    title = "How create a programing language"
    slug = post_service.generate_slug(title)
    username = 'testuser'
    content = "BLA BLA BLA"

    user.create(conn, username, "testuser@gmail.com",
                "123456", "123456", "profile text")
    author = user.get_profile(conn, username)
    post_service.create(conn, author.id, title, content)
    post = post_service.get_post_by_slug(conn, username, slug)

    assert post.slug == slug
    assert post.author == username
    assert post.content == content
    assert post.title == title


def test_create_post(conn):
    author = 1
    title = "Pytest test"
    slug = "pytest-test"
    content = "foo"
    username = "username"

    user.create(conn, username, "username@gmail.com",
                "123456", "123456", "profile")
    post_service.create(conn, author, title, content)
    post = post_service.get_post_by_slug(conn, username, slug)

    assert post.title == title
    assert post.slug == slug
    assert post.author == username
    assert post.content == content


def test_update_post(conn):
    author = 1
    old_title = "Pytest test"
    old_slug = "pytest-test"
    old_content = "foo"
    new_title = "Pytest test 2"
    new_slug = "pytest-test-2"
    new_content = "bar"
    username = "username"

    user.create(conn, username, "username@gmail.com",
                "123456", "123456", "profile")
    post_service.create(conn, author, old_title, old_content)
    old_post = post_service.get_post_by_slug(conn, username, old_slug)

    post_service.create(conn, author, new_title, new_content)
    new_post = post_service.get_post_by_slug(conn, username, new_slug)

    assert not new_post.content == old_post.content
    assert not new_post.title == old_post.title
    assert not new_post.content == old_post.content


def test_search_posts_when_provide_username_and_all_return_posts_should_be_related_to_requested_author(conn):
    username1 = 'cool_name_1'
    email1 = 'coolname1@gmail.com'

    username2 = 'cool_name_2'
    email2 = 'coolname2@gmail.com'

    password = '123'
    password_repeat = '123'
    profile_text = 'this is some random profile text'
    user.create(
        conn, username1, email1, password, password_repeat, profile_text)
    user.create(
        conn, username2, email2, password, password_repeat, profile_text)
    user1 = user.get_profile(conn, username1)
    user2 = user.get_profile(conn, username2)

    random_title1 = 'title 1'
    random_title2 = 'title 2'
    random_title3 = 'title 3'
    random_content = 'content'
    post1 = post_service.create(
        conn, user1.id, random_title1, random_content)
    post2 = post_service.create(
        conn, user1.id, random_title2, random_content)
    post3 = post_service.create(
        conn, user2.id, random_title3, random_content)

    posts = post_service.get_posts_by_author(conn, username1)

    for post in posts:
        assert post.author == username1


def test_if_total_posts_of_search_posts_when_provide_username_is_less_than_total_posts_exists_in_database(conn):
    username1 = 'cool_name_1'
    email1 = 'coolname1@gmail.com'

    username2 = 'cool_name_2'
    email2 = 'coolname2@gmail.com'

    password = '123'
    password_repeat = '123'
    profile_text = 'this is some random profile text'
    user.create(
        conn, username1, email1, password, password_repeat, profile_text)
    user.create(
        conn, username2, email2, password, password_repeat, profile_text)

    user1 = user.get_profile(conn, username1)
    user2 = user.get_profile(conn, username2)

    random_title1 = 'title 1'
    random_title2 = 'title 2'
    random_title3 = 'title 3'
    random_content = 'content'
    post1 = post_service.create(
        conn, user1.id, random_title1, random_content)
    post2 = post_service.create(
        conn, user1.id, random_title2, random_content)
    post3 = post_service.create(
        conn, user2.id, random_title3, random_content)

    posts = post_service.get_posts_by_author(conn, username1)

    with conn.cursor(cursor_factory=DictCursor) as curs:
        query = "SELECT * FROM posts"
        curs.execute(query)
        rows = curs.fetchall()

    assert len(rows) > len(posts)


def test_user_search_for_post_by_specifc_tag_then_return_posts_with_this_specifc_tag(conn):
    # Create two users
    username1 = 'cool_name_1'
    email1 = 'coolname1@gmail.com'
    username2 = 'cool_name_2'
    email2 = 'coolname2@gmail.com'
    password = '123'
    password_repeat = '123'
    profile_text = 'this is some random profile text'
    user.create(
        conn, username1, email1, password, password_repeat, profile_text)

    # Get the two created users
    user1 = user.get_profile(conn, username1)

    # Create 2 posts
    random_title1 = 'title 1'
    random_title2 = 'title 2'
    random_content = 'content'
    post_service.create(
        conn, user1.id, random_title1, random_content)
    post_service.create(
        conn, user1.id, random_title2, random_content)

    # Create 2 tags
    with conn.cursor(cursor_factory=DictCursor) as cur:
        tag1 = 'ble-ble'
        tag2 = 'ble-bl1'
        query = "INSERT INTO tags (tag) VALUES (%s)"
        cur.execute(query, (tag1, ))
        cur.execute(query, (tag2, ))

    # Create 2 posts_tags
    with conn.cursor(cursor_factory=DictCursor) as cur:
        tag_id_1 = 1
        post_id_1 = 1
        tag_id_2 = 2
        post_id_2 = 2
        query = "INSERT INTO posts_tags (tag_id, post_id) VALUES (%s, %s)"
        cur.execute(query, (tag_id_1, post_id_1))
        cur.execute(query, (tag_id_2, post_id_2))

    tag_searching_for = 'ble-ble'

    posts = post_service.get_posts_by_tag(conn, tag_searching_for)

    assert len(posts) == 1

    for post in posts:
        assert post.title == random_title1


def test_generate_slug():
    temp = [
        {
            'title': "this is WEIRD FuNcTion",
            'want': "this-is-weird-function"
        },
        {
            'title': "#my title <>&#@*(&#!(",
            'want': "my-title"
        },
    ]

    for item in temp:
        assert item['want'] == post_service.generate_slug(item['want'])
