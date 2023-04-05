from flask import Flask
from api.lib.orm import find_all, build_from_record
from api.lib.db import cursor
from api.models.person import Person
import json
import psycopg2

def create_app(db_name):
    app = Flask(__name__)
    app.config.from_mapping(DATABASE = db_name)

    @app.route('/')
    def root_url():
        return "welcome to the adventureworks app"
    
    @app.route('/persons')
    def persons():
        persons = find_all(cursor, Person)
        person_dicts = [person.__dict__ for person in persons]
        return json.dumps(person_dicts, default = str)
    
    @app.route('/persons/lastname/<lastname>')
    def get_persons(lastname):
        conn = psycopg2.connect(dbname = db_name)
        cursor = conn.cursor()
        
        cursor.execute('select * from person.person where lastname = %s', (lastname,))
        records = cursor.fetchall()
        persons = [build_from_record(Person, record) for record in records]
        person_dicts = [person.__dict__ for person in persons]
        return json.dumps(person_dicts, default = str)

    return app
