from flask import redirect, request, render_template
from flask_app import app
from flask_app.models import author
from flask_app.models import book

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'Invalid URL.'

@app.route('/')
def index():
    return redirect('/authors')

@app.route('/authors')
def authors():
    authors = author.Author.get_all_authors()
    return render_template('authors.html', all_authors = authors)

@app.route('/author_show/<int:id>')
def author_show(id):
    data = {
        'id' : id
    }
    an_author = author.Author.get_one_author_with_favorites(data)
    not_fav_books = book.Book.get_unfavorited_books(data)
    return render_template('author_show.html', one_author = an_author, unfavorited_books = not_fav_books)

@app.route('/create_author_submit', methods=['POST'])
def create_author_submit():
    data = {
        'author_name' : request.form['author_name']
    }
    author.Author.new_author(data)
    return redirect('/authors')

@app.route('/create_favorite_submit', methods=['POST'])
def create_favorite_submit():
    data = {
        'author_id' : request.form['author_id'],
        'book_id' : request.form['book_select']
    }
    print(data)
    author.Author.add_favorite(data)
    return redirect(f'/author_show/{request.form["author_id"]}')