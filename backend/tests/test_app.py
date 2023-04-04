import pytest
import json
from api import create_app
from api.models.person import Movie
from api.lib.db import drop_records, get_db, close_db
from api.lib.orm import save


@pytest.fixture(scope = 'module')
def app():
    flask_app = create_app('imdb_movies')

    with flask_app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        drop_records(cursor, conn, 'movies')
        drop_records(cursor, conn, 'actors')
        build_records(conn, cursor)

        conn.commit()
        close_db()
    yield flask_app

    with flask_app.app_context():
        close_db()
        conn = get_db()
        cursor = conn.cursor()
        drop_records(cursor, conn, 'movies')
        drop_records(cursor, conn, 'actors')
        close_db()


def build_records(conn, cursor):
    # cursor.execute(f"ALTER SEQUENCE movies_id_seq RESTART WITH 1;")
    # conn.commit()
    for i in range(1, 15):
        fast_and_furious = Movie(title = f'Fast and Furious: {i}')
        save(fast_and_furious, conn, cursor)
    
    shawshank = Movie(title = 'shawshank')
    save(shawshank, conn, cursor)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_root_url(app, client):
    response = client.get('/')
    assert b'welcome to the imdb movies app' in response.data

def test_movies_url_returns_first_ten_movies(app, client):
    response = client.get('/movies')
    dicts = json.loads(response.data)
    assert len(dicts) == 10

def test_movies_show_returns_the_specified_movie(app, client):
    response = client.get('/movies/shawshank')
    movie_dict = json.loads(response.data)
    assert movie_dict['title'] == 'shawshank'
    # assert movie_dict['title'] == 'Fast and Furious: 2'

