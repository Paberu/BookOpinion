import unittest
import dearpygui.dearpygui as dpg
from Book import Book
from BookOpinion import BookOpinion



class TestBookOpinion(unittest.TestCase):

    def setUp(self):
        # Инициализация DearPyGui перед каждым тестом
        dpg.create_context()

    def tearDown(self):
        # Очистка DearPyGui после каждого теста
        dpg.destroy_context()

    def testCreateBookOpinion(self):
        book_opinion = BookOpinion()
        self.assertIsInstance(book_opinion, BookOpinion)

    def testAddBook(self):
        book_opinion = BookOpinion()
        book = Book(title='1984', author='Orwell', writing_year=1948, rating=9)
        book_opinion.add_book(book)
        test_book = book_opinion.get_books()[0]
        self.assertIsInstance(test_book, Book)
        self.assertEqual(test_book.get_field('title'), '1984')

    def testDeleteBook(self):
        book_opinion = BookOpinion()
        book = Book.create_from_dict({'title': '1984', 'author': 'Orwell', 'writing_year': 1948,
                                      'publication_year': None, 'rating': 9, 'opinion': None})
        book_opinion.add_book(book)
        book_opinion.delete_book()


unittest.main()
