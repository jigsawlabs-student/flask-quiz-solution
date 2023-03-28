from api.models.movie import Movie

def movie_accepts_mass_assignment():
    movie = Movie(title = 'Fast and Furious', runtime = 83)
    assert movie.title == 'Fast and Furious'