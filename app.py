from flask import Flask, redirect, render_template, request, url_for
import requests
from uuid import uuid4

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


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
            '500.html',
            cache_id=uuid4(),
        )


@app.route('/about', strict_slashes=False)
def about():
    if api_status()['status'] == 'OK':
        return render_template(
            'about.html',
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '500.html',
            cache_id=uuid4(),
        )


@app.route('/contact', strict_slashes=False)
def contact():
    if api_status()['status'] == 'OK':
        return render_template(
            'contact.html',
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '500.html',
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
            '500.html',
            cache_id=uuid4(),
        )


@app.route('/admin/signin', strict_slashes=False)
def admin_signin():
    if api_status()['status'] == 'OK':
        return render_template(
            'admin/signin.html',
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '500.html',
            cache_id=uuid4(),
        )


@ app.route('/admin/authors', strict_slashes=False)
def admin_authors():
    if api_status()['status'] == 'OK':
        return render_template(
            'admin/authors.html',
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '500.html',
            cache_id=uuid4(),
        )


@ app.route('/admin/books', strict_slashes=False)
def admin_books():
    return render_template(
        'admin/books.html',
        cache_id=uuid4(),
    )


@ app.route('/admin/languages', strict_slashes=False)
def admin_languages():
    if api_status()['status'] == 'OK':
        return render_template(
            'admin/languages.html',
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '500.html',
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
            '500.html',
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
            '500.html',
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
            '500.html',
            cache_id=uuid4(),
        )


@app.route('/discover', strict_slashes=False)
def discover():
    if api_status()['status'] == 'OK':
        return render_template(
            'discover.html',
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '500.html',
            cache_id=uuid4(),
        )


@app.route('/library', strict_slashes=False)
def library():
    if api_status()['status'] == 'OK':
        return render_template(
            'library.html',
            cache_id=uuid4(),
        )
    else:
        return render_template(
            '500.html',
            cache_id=uuid4(),
        )


# @app.route('/author/<author_id>', strict_slashes=False)
# def author(author_id):
#     if api_status()['status'] == 'OK':
#         return render_template(
#             'author.html',
#             cache_id=uuid4(),
#         )
#     else:
#         return render_template(
#             '500.html',
#             cache_id=uuid4(),
#         )


# @app.route('/book/<book_id>', strict_slashes=False)
# def book(book_id):
#     if api_status()['status'] == 'OK':
#         return render_template(
#             'book.html',
#             cache_id=uuid4(),
#         )
#     else:
#         return render_template(
#             '500.html',
#             cache_id=uuid4(),
#       )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
