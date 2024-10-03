class User:
    def __init__(self, user_id: str, name: str, email: str):
        self.__user_id = user_id
        self.__name = name
        self.__email = email

    @property
    def user_id(self):
        return self.__user_id

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email
