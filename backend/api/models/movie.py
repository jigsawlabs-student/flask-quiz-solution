class Movie:
    __table__ = 'movies'
    columns = ["id", "title", "studio", "runtime",
                "description", "release_date", "year"]
    
    def __init__(self, **args):
        self.__dict__ = args