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
        return "welcome to the imdb movies app"
    
    @app.route('/movies')
    def movies():
        movies = find_all(cursor, Movie)
        movie_dicts = [movie.__dict__ for movie in movies]
        
        return json.dumps(movie_dicts, default = str)
    
    @app.route('/movies/<title>')
    def get_movie(title):
        conn = psycopg2.connect(dbname = db_name)
        cursor = conn.cursor()
        
        cursor.execute('select * from movies where title = %s', (title,))
        record = cursor.fetchone()
        movie = build_from_record(Movie, record)
        return json.dumps(movie.__dict__, default = str)

    return app
