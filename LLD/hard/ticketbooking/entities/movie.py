class Movie:
    def __init__(self, movie_id: str, title: str, description: str, duration: int):
        self.__movie_id = movie_id
        self.__title = title
        self.__description = description
        self.__duration = duration  # in minutes

    @property
    def movie_id(self):
        return self.__movie_id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def duration(self):
        return self.__duration

    def __str__(self):
        return f"{self.__title} ({self.__duration} mins)"
