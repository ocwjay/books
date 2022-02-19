from flask import redirect, request, render_template
from flask_app import app
from flask_app.models import book
from flask_app.models import author

@app.route('/books')
def books():
    books = book.Book.get_all_books()
    return render_template('books.html', all_books = books)

@app.route('/book_show/<int:id>')
def book_show(id):
    data = {
        'id' : id
    }
    a_book = book.Book.get_one_book_with_authors(data)
    not_fav_authors = author.Author.get_unfavorited_authors(data)
    return render_template('book_show.html', one_book = a_book, unfavorited_authors = not_fav_authors)

@app.route('/new_book_submit', methods=['POST'])
def new_book_submit():
    data = {
        'title' : request.form['title'],
        'num_of_pages' : request.form['num_of_pages']
    }
    book.Book.new_book(data)
    return redirect('/books')

@app.route('/create_favorite_book_submit', methods=['POST'])
def create_favorite_book_submit():
    data = {
        'author_id' : request.form['author_select'],
        'book_id' : request.form['book_id']
    }
    print(data)
    author.Author.add_favorite(data)
    return redirect(f'/book_show/{request.form["book_id"]}')