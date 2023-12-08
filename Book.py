class Book:
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
        setattr(self, field_name, value)

    def get_values(self):
        return self.title, self.author, self.writing_year, self.publication_year, self.rating, self.opinion

    def convert_to_dict(self):
        book_dict = {'title': self.title, 'author': self.author, 'writing_year': self.writing_year,
                     'publication_year': self.publication_year, 'rating': self.rating, 'opinion': self.opinion}
        return book_dict
    @classmethod
    def create_from_dict(cls, book_dict):
        book = cls(
            title = book_dict['title'],
            author = book_dict['author'],
            writing_year = book_dict['writing_year'],
            publication_year = book_dict['publication_year'],
            rating = book_dict['rating'],
            opinion = book_dict['opinion'])
        return book