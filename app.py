from flask import Flask, redirect, render_template, request, url_for
import json
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
        cache_id = uuid4()
        return render_template(
            'index.html',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@app.route('/about', strict_slashes=False)
def about():
    if api_status()['status'] == 'OK':
        cache_id = uuid4()
        return render_template(
            'about.html',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@app.route('/contact', strict_slashes=False)
def contact():
    if api_status()['status'] == 'OK':
        cache_id = uuid4()
        fulll_name = request.form.get('full_name')
        email = request.form.get('email')
        message = request.form.get('message')
        payload = {
            'full_name': fulll_name,
            'email': email,
            'message': message,
        }
        headers = {'Content-Type': 'application/json'}
        url = "http://localhost/api/v1/feedbacks"
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        r_data = r.json()
        if r_data.get('error'):
            return render_template(
                'index.html',
                cache_id=cache_id,
                message=r_data.get('error'))
        return render_template(
            'contact.html',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/admin', strict_slashes=False)
def admin_dashboard():
    if api_status()['status'] == 'OK':
        url = 'http://localhost/api/v1/stats'
        response = requests.get(url).json()
        audiobooks = response['audiobooks']
        authors = response['authors']
        books = response['books']
        categories = response['categories']
        feedbacks = response['feedbacks']
        languages = response['languages']
        narrators = response['narrators']
        reviews = response['reviews']
        users = response['users']
        cache_id = uuid4()
        return render_template(
            'admin/index.html',
            audiobooks=audiobooks,
            authors=authors,
            books=books,
            categories=categories,
            feedbacks=feedbacks,
            languages=languages,
            narrators=narrators,
            reviews=reviews,
            users=users,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/admin/signin', strict_slashes=False)
def admin_signin():
    if api_status()['status'] == 'OK':
        url = "http://localhost/auth/signin"
        cache_id = uuid4()
        return render_template(
            'admin/signin.html',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/admin/audiobooks', strict_slashes=False)
def admin_audiobooks():
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/audiobooks"
        audiobooks = requests.get(url).json()
        cache_id = uuid4()
        return render_template(
            'admin/audiobooks.html',
            audiobooks=audiobooks,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/admin/authors', strict_slashes=False)
def admin_authors():
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/authors"
        authors = requests.get(url).json()
        cache_id = uuid4()
        return render_template(
            'admin/authors.html',
            authors=authors,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/admin/books', strict_slashes=False)
def admin_books():
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/books"
        books = requests.get(url).json()
        cache_id = uuid4()
        return render_template(
            'admin/books.html',
            books=books,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/admin/categories', strict_slashes=False)
def admin_categories():
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/categories"
        categories = requests.get(url).json()
        cache_id = uuid4()
        return render_template(
            'admin/categories.html',
            categories=categories,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/admin/feedbacks', strict_slashes=False)
def admin_feedbacks():
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/feedbacks"
        feedbacks = requests.get(url).json()
        cache_id = uuid4()
        return render_template(
            'admin/feedbacks.html',
            feedbacks=feedbacks,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/admin/languages', strict_slashes=False)
def admin_languages():
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/languages"
        languages = requests.get(url).json()
        cache_id = uuid4()
        return render_template(
            'admin/languages.html',
            languages=languages,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/admin/narrators', strict_slashes=False)
def admin_narrators():
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/narrators"
        narrators = requests.get(url).json()
        cache_id = uuid4()
        return render_template(
            'admin/narrators.html',
            narrators=narrators,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/admin/reviews', strict_slashes=False)
def admin_reviews():
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/reviews"
        reviews = requests.get(url).json()
        cache_id = uuid4()
        return render_template(
            'admin/reviews.html',
            reviews=reviews,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/admin/users', strict_slashes=False)
def admin_users():
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/users"
        users = requests.get(url).json()
        cache_id = uuid4()
        return render_template(
            'admin/users.html',
            users=users,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/signin', strict_slashes=False)
def signin():
    if api_status()['status'] == 'OK':
        url = "http://localhost/auth/signin"
        cache_id = uuid4()
        return render_template(
            'signin.html',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/signup', strict_slashes=False)
def signup():
    if api_status()['status'] == 'OK':
        url = "http://localhost/auth/signup"
        cache_id = uuid4()
        return render_template(
            'signup.html',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/discover', strict_slashes=False)
def discover():
    if api_status()['status'] == 'OK':
        cache_id = uuid4()
        url = "http://localhost/api/v1/books"
        books = requests.get(url).json()
        return render_template(
            'discover.html',
            books=books,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/library', strict_slashes=False)
def library():
    if api_status()['status'] == 'OK':
        cache_id = uuid4()
        return render_template(
            'library.html',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@app.route('/author', strict_slashes=False)
def author():
    if api_status()['status'] == 'OK':
        cache_id = uuid4()
        return redirect(url_for('discover'))
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/author/<author_id>', strict_slashes=False)
def get_author(author_id):
    if api_status()['status'] == 'OK':
        cache_id = uuid4()
        url = "http://localhost/api/v1/authors/" + author_id
        books = requests.get("http://localhost/api/v1/books/").json()
        author = requests.get(url).json()
        return render_template(
            'author.html',
            author=author,
            books=books,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/book', strict_slashes=False)
def book():
    if api_status()['status'] == 'OK':
        cache_id = uuid4()
        return redirect(url_for('discover'))
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/book/<book_id>', strict_slashes=False)
def get_book(book_id):
    if api_status()['status'] == 'OK':
        cache_id = uuid4()
        url = "http://localhost/api/v1/books/" + book_id
        book = requests.get(url).json()
        authors = requests.get("http://localhost/api/v1/authors").json()
        return render_template(
            'book.html',
            book=book,
            authors=authors,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
