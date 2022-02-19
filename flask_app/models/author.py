from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []
    @classmethod
    def new_author(cls, data):
        query = "INSERT INTO authors(name) VALUE (%(author_name)s)"
        results = connectToMySQL('books_schema').query_db(query, data)
        return results
    @classmethod
    def get_all_authors(cls):
        query = "SELECT * FROM authors"
        results = connectToMySQL('books_schema').query_db(query)
        authors = []
        for author in results:
            authors.append(cls(author))
        return authors
    @classmethod
    def get_one_author_with_favorites(cls, data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s"
        results = connectToMySQL('books_schema').query_db(query, data)
        author = cls(results[0])
        print(results)
        for db_row in results:
            book_model = {
                'id' : db_row['books.id'],
                'title' : db_row['title'],
                'num_of_pages' : db_row['num_of_pages'],
                'created_at' : db_row['books.created_at'],
                'updated_at' : db_row['books.updated_at']
            }
            author.books.append(book.Book(book_model))
        return author
    @classmethod
    def add_favorite(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUE (%(author_id)s, %(book_id)s)"
        results = connectToMySQL('books_schema').query_db(query, data)
        return results
    @classmethod
    def get_unfavorited_authors(cls, data):
        query = "SELECT * FROM authors WHERE authors.id NOT IN ( SELECT author_id FROM favorites WHERE book_id = %(id)s );"
        results = connectToMySQL('books_schema').query_db(query, data)
        authors = []
        for db_row in results:
            authors.append(cls(db_row))
        return authors