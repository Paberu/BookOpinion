import unittest
import dearpygui.dearpygui as dpg
from Book import Book
from BookOpinion import BookOpinion



class TestBookOpinion(unittest.TestCase):

    def setUp(self):
        self.book_opinion = BookOpinion()

    def testCreateBookOpinion(self):
        self.assertIsInstance(self.book_opinion, BookOpinion)

    def testAddBook(self):
        book = Book(title='1984', author='Orwell', writing_year=1948, rating=9)
        self.book_opinion.add_to_books(book)
        test_book = self.book_opinion.get_books()[0]
        self.assertIsInstance(test_book, Book)
        self.assertEqual(test_book.get_field('_Book__title'), '1984')

    def testDeleteFromBooks(self):
        book = Book.create_from_dict({'title': '1984', 'author': 'Orwell', 'writing_year': 1948,
                                      'publication_year': None, 'rating': 9, 'opinion': None})
        self.book_opinion.add_to_books(book)
        self.book_opinion.delete_from_books(book)
        self.assertEqual(self.book_opinion.get_books(), [])


unittest.main()
