class Book:

    BOOK_FIELDS = ('title', 'author', 'writing_year', 'publication_year', 'rating', 'opinion')

    def __init__(self, title, author, writing_year=None, publication_year=None, rating=None, opinion=None):
        self.title = title
        self.author = author
        self.writing_year = writing_year
        self.publication_year = publication_year
        self.rating = rating
        self.opinion = opinion

    def get_field(self, field_name):
        return getattr(self, field_name)

    def set_field(self, field_name, value):
        if field_name in self.BOOK_FIELDS:
            setattr(self, field_name, value)
        else:
            raise AttributeError('Нельзя создавать новые поля')

    def __str__(self):
        return self.title

    def get_values(self):
        return self.title, self.author, self.writing_year, self.publication_year, self.rating, self.opinion

    def convert_to_dict(self):
        book_dict = {'title': self.title, 'author': self.author, 'writing_year': self.writing_year,
                     'publication_year': self.publication_year, 'rating': self.rating, 'opinion': self.opinion}
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
        if not Book.check_year(self.writing_year):
            self.writing_year = ''
        if not Book.check_year(self.publication_year):
            self.publication_year = ''
