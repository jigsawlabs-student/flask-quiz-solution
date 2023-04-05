import pytest
import json
from api import create_app
from api.models.person import Person
from api.lib.db import drop_records, get_db, close_db, test_conn, test_cursor, save
from settings import TEST_DB_NAME


@pytest.fixture(scope = 'module')
def app():
    flask_app = create_app(TEST_DB_NAME)

    with flask_app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        drop_records(cursor, conn, 'person.person')
        build_records(conn, cursor)

        conn.commit()
        close_db()
    yield flask_app

    with flask_app.app_context():
        close_db()
        conn = get_db()
        cursor = conn.cursor()
        drop_records(cursor, conn, 'person.person')
        close_db()

def build_records(conn, cursor):
    for i in range(1, 12):
        sam = Person(firstname =f'Sam {i}', lastname = 'ok', businessentityid = i, persontype = 'EM')
        save(sam, conn, cursor)
    bob = Person(firstname =f'Bob', lastname = 'not ok', businessentityid = i, persontype = 'EM')
    save(bob, conn, cursor)

@pytest.fixture()
def build_people():
    
    drop_records(test_cursor, test_conn, 'person.person')
    build_records(test_conn, test_cursor)

    yield

    drop_records(test_cursor, test_conn, 'person.person')

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_root_url(app, client):
    response = client.get('/')
    assert b'welcome to the adventureworks app' in response.data

def test_persons_url_returns_first_ten_people(app, client):
    response = client.get('/persons')
    dicts = json.loads(response.data)
    assert len(dicts) == 10

def test_persons_last_name_returns_all_of_matching_last_name(app, client):
    response = client.get('/persons/lastname/ok')
    person_response = json.loads(response.data)
    assert len(person_response) == 11
    

