class Book:

    BOOK_FIELDS = ('_Book__title', '_Book__author', '_Book__writing_year',
                   '_Book__publication_year', '_Book__rating', '_Book__opinion')

    def __init__(self, title, author, writing_year=None, publication_year=None, rating=None, opinion=None):
        self.__title = title
        self.__author = author
        self.__writing_year = writing_year
        self.__publication_year = publication_year
        self.__rating = rating
        self.__opinion = opinion

    def get_field(self, field_name):
        if field_name not in self.BOOK_FIELDS:
            raise AttributeError('Нельзя создавать новые поля')
        return getattr(self, field_name)

    def set_field(self, field_name, value):
        if field_name not in self.BOOK_FIELDS:
            raise AttributeError('Нельзя создавать новые поля')
        setattr(self, field_name, value)

    def __str__(self):
        return self.__title

    def get_values(self):
        return self.__title, self.__author, self.__writing_year, self.__publication_year, self.__rating, self.__opinion

    def convert_to_dict(self):
        book_dict = {'title': self.__title, 'author': self.__author, 'writing_year': self.__writing_year,
                     'publication_year': self.__publication_year, 'rating': self.__rating, 'opinion': self.__opinion}
        return book_dict

    @classmethod
    def create_from_dict(cls, book_dict):
        book = cls(
            title=book_dict['title'],
            author=book_dict['author'],
            writing_year=book_dict['writing_year'],
            publication_year=book_dict['publication_year'],
            rating=book_dict['rating'],
            opinion=book_dict['opinion'])
        return book

    @classmethod
    def check_year(cls, argument):
        argument = str(argument)
        for i in range(len(argument) - 3):
            if argument[i:i + 4].isdigit():
                return True
        return False

    def check_years(self):
        if not Book.check_year(self.__writing_year):
            self.__writing_year = ''
        if not Book.check_year(self.__publication_year):
            self.__publication_year = ''
