from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []
    @classmethod
    def new_book(cls, data):
        query = "INSERT INTO books(title, num_of_pages) VALUE(%(title)s, %(num_of_pages)s);"
        results = connectToMySQL('books_schema').query_db(query, data)
        return results
    @classmethod
    def get_all_books(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL('books_schema').query_db(query)
        books = []
        for book in results:
            books.append(cls(book))
        return books
    @classmethod
    def get_one_book_with_authors(cls, data):
        # query = "SELECT * FROM favorites JOIN books ON books.id = favorites.book_id JOIN authors on authors.id = favorites.author_id WHERE books.id = %(id)s;"
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s"
        results = connectToMySQL('books_schema').query_db(query, data)
        book = cls(results[0])
        for db_row in results:
            author_model = {
                'id' : db_row['authors.id'],
                'name' : db_row['name'],
                'created_at' : db_row['authors.created_at'],
                'updated_at' : db_row['authors.updated_at']
            }
            book.authors.append(author.Author(author_model))
        return book
    @classmethod
    def get_unfavorited_books(cls, data):
        query = "SELECT * FROM books WHERE books.id NOT IN ( SELECT book_id FROM favorites WHERE author_id = %(id)s );"
        results = connectToMySQL('books_schema').query_db(query, data)
        books = []
        for db_row in results:
            books.append(cls(db_row))
        return books
