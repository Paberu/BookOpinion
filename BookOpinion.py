import dearpygui.dearpygui as dpg
import json

from Book import Book


class BookOpinion:
    BASE_NAME = 'book_collection.json'

    def __init__(self):
        self.books = []
        self.titles = []
        self.current_book = None
        self.gui = dpg

    def fill_the_gui(self):
        with self.gui.window(label='Список книг', tag='bookcase', no_close=True, width=BOOKSHELF_WIDTH, height=APP_HEIGHT):
            with self.gui.group(horizontal=True):
                self.gui.add_button(label='Добавить книгу', callback=self.create_book)
                self.gui.add_button(label='Сохранить в файл', callback=self.save_to_file)
                self.gui.add_button(label='Загрузить из файла', callback=self.load_from_file)
            self.gui.add_listbox(items=book_opinion.books, width=BOOKSHELF_WIDTH, num_items=APP_HEIGHT // 30,
                                 callback=self.choose_book, tag='bookshelf', show=True)

        with self.gui.window(label='Информация о книге', tag='book_info', no_close=True, pos=(BOOKSHELF_WIDTH, 0),
                        width=BOOK_PROPERTIES_WIDTH, height=APP_HEIGHT):
            title = self.gui.add_input_text(tag='book_title', hint='Название книги', width=BOOK_PROPERTIES_WIDTH)
            author = self.gui.add_input_text(tag='book_author', hint='Автор', width=BOOK_PROPERTIES_WIDTH)
            writing_year = self.gui.add_input_text(tag='book_written', hint='Год написания книги',
                                              width=BOOK_PROPERTIES_WIDTH // 3)
            publication_year = self.gui.add_input_text(tag='book_published', hint='Год издания книги',
                                                  width=BOOK_PROPERTIES_WIDTH // 3)
            rating = self.gui.add_slider_int(tag='rating', min_value=0, max_value=10, width=BOOK_PROPERTIES_WIDTH // 3)
            self.gui.add_text('Напишите Ваше мнение о книге или целый обзор:')
            opinion = self.gui.add_input_text(tag='book_opinion', multiline=True, width=BOOK_PROPERTIES_WIDTH, height=200)
            with self.gui.group(horizontal=True):
                self.gui.add_button(label='Сохранить книгу', callback=self.save_book,
                               user_data=[title, author, writing_year, publication_year, rating, opinion])
                self.gui.add_button(label='Отменить', callback=self.cancel_book_editing,
                               user_data=[title, author, writing_year, publication_year, rating, opinion])
                self.gui.add_button(label='Удалить', callback=self.delete_book,
                                    user_data=[title, author, writing_year, publication_year, rating, opinion])

    def get_books(self):
        return self.books

    def get_titles(self):
        return self.titles

    def add_to_books(self, book):
        self.books.append(book)
        self.titles.append(book.get_field('_Book__title'))

    def delete_from_books(self, book):
        self.books.remove(book)
        self.titles.remove(book.get_field('_Book__title'))

    def get_book_by_title(self, title):
        for book in self.books:
            if book.get_field('_Book__title') == title:
                return book

    def pop_book_by_title(self, title):
        for book in self.books:
            if book.get_field('_Book__title') == title:
                self.books.remove(book)
                return book

    def save_to_file(self):
        with open(self.BASE_NAME, 'w') as fp:
            for book in self.books:
                json.dump(book.convert_to_dict(), fp)
                fp.write('\n')

    def load_from_file(self):
        with open(self.BASE_NAME, 'r') as fp:
            json_line = fp.readline()
            while json_line:
                book_dict = json.loads(json_line)
                book = Book.create_from_dict(book_dict)
                self.books.append(book)
                self.titles.append(book.get_field('_Book__title'))
                json_line = fp.readline()
        dpg.configure_item('bookshelf', items=book_opinion.books)

    def create_book_dict_from_user_data(self, user_data):
        book_dict = {
            'title': dpg.get_value(user_data[0]),
            'author': dpg.get_value(user_data[1]),
            'writing_year': dpg.get_value(user_data[2]),
            'publication_year': dpg.get_value(user_data[3]),
            'rating': dpg.get_value(user_data[4]),
            'opinion': dpg.get_value(user_data[5])
        }
        return book_dict

    def create_book(self, sender, data):
        dpg.configure_item('book_title', default_value='', hint='Название книги')
        dpg.configure_item('book_author', default_value='', hint='Автор')
        dpg.configure_item('book_written', default_value='', hint='Год написания книги')
        dpg.configure_item('book_published', default_value='', hint='Год издания книги')
        dpg.configure_item('rating', default_value=5)
        dpg.configure_item('book_opinion', default_value='Ваше мнение/обзор')
        book_opinion.current_book = None

    def save_book(self, sender, data, user_data):
        title = dpg.get_value(user_data[0])
        if title in ('', ' ', None):
            with dpg.window(label='Ошибка при сохранении книги', modal=True, no_close=True, tag='warning'):
                dpg.add_text('Вы не задали название книги или в программе произошёл сбой. Проверьте имеющиеся данные.')
                dpg.add_button(label='Понятно', callback=self.edit_again, user_data=user_data)
            return
        if title not in book_opinion.titles:
            self.save_anyway(sender, data, user_data)
            return
        if title in book_opinion.titles:
            with dpg.window(label='Ошибка при сохранении книги', modal=True, no_close=True, tag='warning'):
                dpg.add_text(f'Книга с названием "{title}" уже есть. Что надо сделать?')
                with dpg.group(horizontal=True):
                    dpg.add_button(label='Сохранить вместо старого', tag='save_anyway', callback=self.save_anyway, user_data=user_data)
                    dpg.add_button(label='Нет, я изменю название книги', tag='edit', callback=self.edit_again, user_data=user_data)
            return

    def save_anyway(self, sender, data, user_data):
        new_book = Book.create_from_dict(self.create_book_dict_from_user_data(user_data))
        if sender == 'save_anyway':
            book_opinion.pop_book_by_title(new_book.get_field('_Book__title'))
            dpg.delete_item('warning')
        new_book.check_years()
        book_opinion.add_to_books(new_book)
        book_opinion.current_book = new_book
        dpg.configure_item('bookshelf', items=book_opinion.books)

    def edit_again(self, sender, data, user_data):
        book_dict = self.create_book_dict_from_user_data(user_data)
        dpg.configure_item('book_title', default_value=book_dict['title'])
        dpg.configure_item('book_author', default_value=book_dict['author'])
        dpg.configure_item('book_written', default_value=book_dict['writing_year'])
        dpg.configure_item('book_published', default_value=book_dict['publication_year'])
        dpg.configure_item('rating', default_value=book_dict['rating'])
        dpg.configure_item('book_opinion', default_value=book_dict['opinion'])
        dpg.delete_item('warning')

    def choose_book(self, sender, data):
        chosen_book = book_opinion.current_book = book_opinion.get_book_by_title(data)
        dpg.configure_item('book_title', default_value=chosen_book.get_field('_Book__title'))
        dpg.configure_item('book_author', default_value=chosen_book.get_field('_Book__author'))
        dpg.configure_item('book_written', default_value=chosen_book.get_field('_Book__writing_year'))
        dpg.configure_item('book_published', default_value=chosen_book.get_field('_Book__publication_year'))
        dpg.configure_item('rating', default_value=chosen_book.get_field('_Book__rating'))
        dpg.configure_item('book_opinion', default_value=chosen_book.get_field('_Book__opinion'))

    def cancel_book_editing(self, sender, data, user_data):
        self.create_book(sender, data)

    def delete_book(self, sender, data, user_data):
        book_dict = self.create_book_dict_from_user_data(user_data)
        book_opinion.pop_book_by_title(book_dict['title'])
        dpg.configure_item('bookshelf', items=book_opinion.books)
        self.create_book(sender, data)


if __name__ == '__main__':
    book_opinion = BookOpinion()

    FONT_SIZE = 14
    APP_HEIGHT = 900
    APP_WIDTH = 1200
    BOOKSHELF_WIDTH = APP_WIDTH // 3
    BOOK_PROPERTIES_WIDTH = APP_WIDTH * 2 // 3
    LABEL_WIDTH = 100

    book_opinion.gui.create_context()

    with book_opinion.gui.font_registry():
        with book_opinion.gui.font(r'C:\Windows\Fonts\Arial.ttf', FONT_SIZE, default_font=True, id='default_font'):
            book_opinion.gui.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    book_opinion.gui.bind_font('default_font')
    book_opinion.fill_the_gui()
    book_opinion.gui.create_viewport(title='BookOpinion', width=APP_WIDTH, height=APP_HEIGHT)
    book_opinion.gui.setup_dearpygui()
    book_opinion.gui.show_viewport()
    book_opinion.gui.start_dearpygui()

    book_opinion.gui.destroy_context()
