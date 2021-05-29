from app.services import post as post_service, user


def test_get_post_by_slug(conn):
    title = "How create a programing language"
    slug = post_service.generate_slug(title)
    username = 'testuser'
    content = "BLA BLA BLA"

    user.create(conn, username, "testuser@gmail.com", "123456", "123456", "profile text")
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

    user.create(conn, username, "username@gmail.com", "123456", "123456", "profile")
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

    user.create(conn, username, "username@gmail.com", "123456", "123456", "profile")
    post_service.create(conn, author, old_title, old_content)
    old_post = post_service.get_post_by_slug(conn, username, old_slug)

    post_service.create(conn, author, new_title, new_content)
    new_post = post_service.get_post_by_slug(conn, username, new_slug)

    assert not new_post.content == old_post.content
    assert not new_post.title == old_post.title
    assert not new_post.content == old_post.content


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
