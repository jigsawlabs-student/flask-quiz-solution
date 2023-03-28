from flask import Flask
import psycopg2

def create_app(db_name):
    app = Flask(__name__)
    app.config.from_mapping(DATABASE = db_name)

    @app.route('/')
    def root_url():
        return "welcome to the imdb movies app"
    
    @app.route('/movies')
    def movies():
        conn = psycopg2.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute('select * from movies')
    return app
