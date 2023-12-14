import dearpygui.dearpygui as dpg

from Book import Book


class BookOpinion:
    BASE_NAME = 'book_collection.json'
    FONT_SIZE = 14

    def __init__(self):
        self.books = []

    def get_books(self):
        return self.books

    def add_book(self, book):
        self.books.append(book)

    def delete_book(self, book):
        self.books.remove(book)


if __name__ == '__main__':
    book_opinion = BookOpinion()

    def create_book(sender, data):
        with dpg.window(tag='create_book'):
            title = dpg.add_input_text(default_value='Название книги')
            author = dpg.add_input_text(default_value='Автор')
            writing_year = dpg.add_input_text(default_value='Год написания книги')
            publication_year = dpg.add_input_text(default_value='Год издания книги')
            rating = dpg.add_input_int(min_value=0, max_value=10, default_value=5)
            opinion = dpg.add_input_text(default_value='Ваше мнение/обзор')
            dpg.add_button(label='Сохранить книгу', callback=save_book,
                           user_data=[title, author, writing_year, publication_year, rating, opinion])
            dpg.add_button(label='Отменить', callback=cancel)

    def save_book(sender, data, user_data):
        title = dpg.get_value(user_data[0])
        author = dpg.get_value(user_data[1])
        no_title = not title or title == 'Название книги'
        no_author = not author or author == 'Автор'
        if no_title or no_author:
            dpg.delete_item('create_book')
            return
        writing_year = dpg.get_value(user_data[2])
        publication_year = dpg.get_value(user_data[3])
        rating = dpg.get_value(user_data[4])
        opinion = dpg.get_value(user_data[5])

        book_dict = {
            'title': title,
            'author': author,
            'writing_year': writing_year,
            'publication_year': publication_year,
            'rating': rating,
            'opinion': opinion
        }
        new_book = Book.create_from_dict(book_dict)
        new_book.check_years()
        book_opinion.add_book(new_book)
        dpg.configure_item('books', items=book_opinion.books)
        dpg.delete_item('create_book')

    def edit_book(sender, data):
        with dpg.window(tag='edit_book'):
            title = dpg.add_input_text(default_value='Название книги')
            author = dpg.add_input_text(default_value='Автор')
            writing_year = dpg.add_input_text(default_value='Год написания книги')
            publication_year = dpg.add_input_text(default_value='Год издания книги')
            rating = dpg.add_input_int(min_value=0, max_value=10, default_value=5)
            opinion = dpg.add_input_text(default_value='Ваше мнение/обзор')
            dpg.add_button(label='Сохранить книгу', callback=save_book,
                           user_data=[title, author, writing_year, publication_year, rating, opinion])
            dpg.add_button(label='Отменить', callback=cancel)

    def cancel(sender, data):
        dpg.delete_item('create_book')

    dpg.create_context()

    with dpg.font_registry():
        with dpg.font(r'C:\Windows\Fonts\Arial.ttf', book_opinion.FONT_SIZE, default_font=True, id='default_font'):
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    dpg.bind_font('default_font')

    with dpg.window(label='Список книг', no_close=True):
        dpg.add_button(label='Добавить книгу', callback=create_book)
        dpg.add_listbox(items=book_opinion.books, width=450, num_items=14, callback=edit_book, tag='books', show=True)


    dpg.create_viewport(title='BookOpinion')
    dpg.setup_dearpygui()
    # dpg.toggle_viewport_fullscreen()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()