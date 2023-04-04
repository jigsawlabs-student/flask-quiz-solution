from api import create_app
app = create_app('imdb_movies')
app.run(debug = True)