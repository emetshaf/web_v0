from flask import Flask, redirect, render_template, request, url_for
from models import storage
import requests
from uuid import uuid4

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.teardown_appcontext
def close_db(error):
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    cache_id = uuid4()
    return render_template('404.html', cache_id=cache_id), 404


def api_status():
    url = 'http://0.0.0.0/api/v1/status'
    try:
        r = requests.get(url)
        return r.json()
    except Exception:
        return {'status': 'FAIL'}


@app.route('/', strict_slashes=False)
def home():
    if api_status()['status'] == 'OK':
        return render_template(
            'index.html',
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '50x.html',
            cache_id=uuid4(),
        )


@ app.route('/admin', strict_slashes=False)
def admin_dashboard():
    if api_status()['status'] == 'OK':
        return render_template(
            'admin/index.html',
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '50x.html',
            cache_id=uuid4(),
        )


@ app.route('/admin/authors', strict_slashes=False)
def admin_authors():
    if api_status()['status'] == 'OK':
        authors = list(storage.all('Author').values())
        return render_template(
            'admin/authors.html',
            authors=authors,
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '50x.html',
            cache_id=uuid4(),
        )


@ app.route('/admin/books', strict_slashes=False)
def admin_books():
    authors = list(storage.all('Author').values())
    languages = list(storage.all('Language').values())
    books = list(storage.all('Book').values())
    return render_template(
        'admin/books.html',
        authors=authors,
        languages=languages,
        books=books,
        cache_id=uuid4(),
    )


@ app.route('/admin/languages', strict_slashes=False)
def admin_languages():
    if api_status()['status'] == 'OK':
        languages = list(storage.all('Language').values())
        return render_template(
            'admin/languages.html',
            languages=languages,
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '50x.html',
            cache_id=uuid4(),
        )


@ app.route('/admin/users', strict_slashes=False)
def admin_users():
    if api_status()['status'] == 'OK':
        return render_template(
            'admin/users.html',
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '50x.html',
            cache_id=uuid4(),
        )


@ app.route('/signup', strict_slashes=False)
def signup():
    if api_status()['status'] == 'OK':
        return render_template(
            'signup.html',
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '50x.html',
            cache_id=uuid4(),
        )


@ app.route('/signin', strict_slashes=False)
def signin():
    if api_status()['status'] == 'OK':
        return render_template(
            'signin.html',
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '50x.html',
            cache_id=uuid4(),
        )


@app.route('/discover', strict_slashes=False)
def discover():
    if api_status()['status'] == 'OK':
        authors = list(storage.all('Author').values())
        languages = list(storage.all('Language').values())
        books = list(storage.all('Book').values())
        return render_template(
            'discover.html',
            authors=authors,
            books=books,
            languages=languages,
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '50x.html',
            cache_id=uuid4(),
        )


@app.route('/book/<book_id>', strict_slashes=False)
def book(book_id):
    if api_status()['status'] == 'OK':
        book = storage.get('Book', book_id)
        return render_template(
            'book.html',
            book=book,
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '50x.html',
            cache_id=uuid4(),
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
