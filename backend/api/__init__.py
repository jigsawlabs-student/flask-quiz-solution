from flask import Flask
from api.lib.orm import find_all, build_from_record, find
from api.lib.db import get_db
from api.models.person import Person
from api.models.address import Address
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
        conn = get_db()
        cursor = conn.cursor()
        persons = find_all(cursor, Person)
        person_dicts = [person.__dict__ for person in persons]
        return json.dumps(person_dicts, default = str)
    
    @app.route('/persons/lastname/<lastname>')
    def get_persons(lastname):
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('select * from person.person where lastname = %s', (lastname,))
        records = cursor.fetchall()
        persons = [build_from_record(Person, record) for record in records]
        person_dicts = [person.__dict__ for person in persons]
        return json.dumps(person_dicts, default = str)
    
    @app.route('/addresses')
    def addresses():
        conn = get_db()
        cursor = conn.cursor()
        addresses = find_all(cursor, Address)
        address_dicts = [address.__dict__ for address in addresses]
        return json.dumps(address_dicts, default = str)

    @app.route('/person/addresses/<businessentityid>')
    def person_with_addresses(businessentityid):
        conn = get_db()
        cursor = conn.cursor()
        person = find(cursor, Person, businessentityid)
        
        person_json = person.to_json(cursor)
        return json.dumps(person_json, default = str)



    return app
