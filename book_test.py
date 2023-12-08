import unittest
from Book import Book


class TestBook(unittest.TestCase):

    def testInvalidBookConstructor1(self):
        with self.assertRaises(Exception):
            Book()

    def testInvalidBookConstructor2(self):
        with self.assertRaises(Exception):
            Book(title='1984')

    def testInvalidBookConstructor3(self):
        with self.assertRaises(Exception):
            Book(author='Orwell')

    def testValidBookConstructor(self):
        book = Book(title='1984', author='Orwell')
        self.assertEqual(book.get_field('title'), '1984')

    def testValidBookConstructor2(self):
        book = Book(title='1984', author='Orwell', writing_year=1948, rating=9)
        self.assertEqual(book.get_field('author'), 'Orwell')

    def testGetValues(self):
        book = Book(title='1984', author='Orwell', writing_year=1948, rating=9)
        self.assertEqual(book.get_values(), ('1984', 'Orwell', 1948, None, 9, None))

    def testWrongFields(self):
        book = Book(title='1984', author='Orwell', writing_year=1948, rating=9)
        book.set_field('printed_by', 'Alpina Productions')
        self.assertEqual(book.get_field('printed_by'), 'Alpina Productions')

    def testConvertToDict(self):
        book = Book(title='1984', author='Orwell', writing_year=1948, rating=9)
        self.assertEqual(book.convert_to_dict(), {'title': '1984', 'author': 'Orwell', 'writing_year': 1948,
                                                  'publication_year': None, 'rating': 9, 'opinion': None})

    def testCreateFromDict(self):
        book = Book.create_from_dict({'title': '1984', 'author': 'Orwell', 'writing_year': 1948,
                                      'publication_year': None, 'rating': 9, 'opinion': None})
        self.assertEqual(book.get_values(), ('1984', 'Orwell', 1948, None, 9, None))\


    def testLeaveOpinion(self):
        book = Book.create_from_dict({'title': '1984', 'author': 'Orwell', 'writing_year': 1948,
                                      'publication_year': None, 'rating': 9, 'opinion': None})
        opinion = f'Прекрасная книга, буду советовать всем!'
        book.set_field('opinion', opinion)
        self.assertEqual(book.convert_to_dict(), {'title': '1984', 'author': 'Orwell', 'writing_year': 1948,
                                                  'publication_year': None, 'rating': 9,
                                                  'opinion': f'Прекрасная книга, буду советовать всем!'})


unittest.main()
