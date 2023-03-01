from flask import Flask, redirect, render_template, request, url_for
import json
import requests
from uuid import uuid4
import logging

logging.basicConfig(level=logging.DEBUG, filename='web.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@ app.errorhandler(404)
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


@ app.route('/', strict_slashes=False)
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


@ app.route('/about', strict_slashes=False)
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


@ app.route('/contact', strict_slashes=False)
def contact():
    if api_status()['status'] == 'OK':
        cache_id = uuid4()
        return render_template(
            'contact.html',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/create_feedback', methods=['POST'], strict_slashes=False)
def create_ffeedback():
    if request.method == 'POST':
        url = "http://localhost/api/v1/feedbacks/"
        full_name = request.form['full_name']
        email = request.form['email']
        message = request.form['message']
        payload = {
            'full_name': full_name,
            'email': email,
            'message': message
        }
        requests.post(url, json=payload)
        return redirect('/contact')


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


@ app.route('/admin/signin', methods=['GET', 'POST'], strict_slashes=False)
def admin_signin():
    if api_status()['status'] == 'OK':
        url = "http://localhost/auth/signin"
        if request.method == 'POST':
            username = request.form.get('username', None)
            password = request.form.get('password', None)
            payload = {
                "username": username,
                "password": password
            }
            headers = {
                'content-type': 'application/json'
            }
            r = requests.post(url, headers=headers,
                              data=json.dumps(payload))
            r_data = r.json()
            if r_data.get('error'):
                return redirect('/admin/signin')
            auth_token = r_data.get('auth_token')
            if auth_token is None:
                return redirect('/admin/signin')
            headers = {'Authorization': 'access_token {}'.format(
                auth_token)}
            res = requests.get(
                "http://localhost/auth/status",
                headers=headers)
            res_data = res.json()
            data = res_data.get('data')
            username = data['username']
            response = requests.get("http://localhost/api/v1/stats").json()
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
                username=username,
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


@ app.route('/admin/create_audiobook', methods=['POST'], strict_slashes=False)
def create_audiobook():
    if request.method == 'POST':
        url = "http://localhost/api/v1/audiobooks/"
        file = request.form['file']
        payload = {'file': file}
        requests.post(url, json=payload)
        return redirect('/admin/audiobooks')


@ app.route('/admin/delete_audiobook/<audiobook_id>', strict_slashes=False)
def delete_audiobook(audiobook_id):
    url = "http://localhost/api/v1/audiobooks/" + audiobook_id
    requests.delete(url)
    return redirect('/admin/audiobooks')


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


@ app.route('/admin/create_author', methods=['POST'], strict_slashes=False)
def create_author():
    if request.method == 'POST':
        url = "http://localhost/api/v1/authors/"
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        payload = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name
        }
        requests.post(url, json=payload)
        return redirect('/admin/authors')


@ app.route('/admin/delete_author/<author_id>', strict_slashes=False)
def delete_author(author_id):
    url = "http://localhost/api/v1/authors/" + author_id
    requests.delete(url)
    return redirect('/admin/authors')


@ app.route('/admin/books', strict_slashes=False)
def admin_books():
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/books"
        books = requests.get(url).json()
        languages = requests.get("http://localhost/api/v1/languages").json()
        cache_id = uuid4()
        return render_template(
            'admin/books.html',
            books=books,
            languages=languages,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/admin/create_book', methods=['POST'], strict_slashes=False)
def create_book():
    if request.method == 'POST':
        url = "http://localhost/api/v1/books/"
        title = request.form['title']
        description = request.form['description']
        language_id = request.form['language']
        payload = {
            'title': title,
            'description': description,
            'language_id': language_id
        }
        requests.post(url, json=payload)
        return redirect('/admin/books')


@ app.route('/admin/delete_book/<book_id>', strict_slashes=False)
def delete_book(book_id):
    url = "http://localhost/api/v1/books/" + book_id
    requests.delete(url)
    return redirect('/admin/books')


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


@ app.route('/admin/create_category', methods=['POST'], strict_slashes=False)
def create_category():
    if request.method == 'POST':
        url = "http://localhost/api/v1/categories/"
        name = request.form['name']
        payload = {
            'name': name
        }
        requests.post(url, json=payload)
        return redirect('/admin/categories')


@ app.route('/admin/delete_category/<category_id>', strict_slashes=False)
def delete_category(category_id):
    url = "http://localhost/api/v1/categories/" + category_id
    requests.delete(url)
    return redirect('/admin/categories')


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


@ app.route('/admin/create_feedback', methods=['POST'], strict_slashes=False)
def create_feedback():
    if request.method == 'POST':
        url = "http://localhost/api/v1/feedbacks/"
        full_name = request.form['full_name']
        email = request.form['email']
        message = request.form['message']
        payload = {
            'full_name': full_name,
            'email': email,
            'message': message
        }
        requests.post(url, json=payload)
        return redirect('/admin/feedbacks')


@ app.route('/admin/delete_feedback/<feedback_id>', strict_slashes=False)
def delete_feedback(feedback_id):
    url = "http://localhost/api/v1/feedbacks/" + feedback_id
    requests.delete(url)
    return redirect('/admin/feedbacks')


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


@ app.route('/admin/create_language', methods=['POST'], strict_slashes=False)
def create_language():
    if request.method == 'POST':
        url = "http://localhost/api/v1/languages/"
        name = request.form['name']
        payload = {
            'name': name
        }
        requests.post(url, json=payload)
        return redirect('/admin/languages')


@ app.route('/admin/delete_language/<language_id>', strict_slashes=False)
def delete_language(language_id):
    url = "http://localhost/api/v1/languages/" + language_id
    requests.delete(url)
    return redirect('/admin/languages')


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


@ app.route('/admin/create_narrator', methods=['POST'], strict_slashes=False)
def create_narrator():
    if request.method == 'POST':
        url = "http://localhost/api/v1/narrators/"
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        payload = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name
        }
        requests.post(url, json=payload)
        return redirect('/admin/narrators')


@ app.route('/admin/delete_narrator/<narrator_id>', strict_slashes=False)
def delete_narrator(narrator_id):
    url = "http://localhost/api/v1/narrators/" + narrator_id
    requests.delete(url)
    return redirect('/admin/narrators')


@ app.route('/admin/reviews', strict_slashes=False)
def admin_reviews():
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/reviews"
        reviews = requests.get(url).json()
        users = requests.get("http://localhost/api/v1/users").json()
        books = requests.get("http://localhost/api/v1/books").json()
        cache_id = uuid4()
        return render_template(
            'admin/reviews.html',
            reviews=reviews,
            users=users,
            books=books,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ app.route('/admin/create_review', methods=['POST'], strict_slashes=False)
def create_review():
    if request.method == 'POST':
        url = "http://localhost/api/v1/reviews/"
        text = request.form['text']
        user_id = request.form['user']
        book_id = request.form['book']
        payload = {
            'text': text,
            'user_id': user_id,
            'book_id': book_id
        }
        requests.post(url, json=payload)
        return redirect('/admin/reviews')


@ app.route('/admin/delete_review/<review_id>', strict_slashes=False)
def delete_review(review_id):
    url = "http://localhost/api/v1/reviews/" + review_id
    requests.delete(url)
    return redirect('/admin/reviews')


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


@ app.route('/admin/create_user', methods=['POST'], strict_slashes=False)
def create_user():
    if request.method == 'POST':
        url = "http://localhost/api/v1/users/"
        username = request.form['username']
        password = request.form['password']
        payload = {
            'username': username,
            'password': password
        }
        requests.post(url, json=payload)
        return redirect('/admin/users')


@ app.route('/admin/delete_user/<user_id>', strict_slashes=False)
def delete_user(user_id):
    url = "http://localhost/api/v1/users/" + user_id
    requests.delete(url)
    return redirect('/admin/users')


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


@ app.route('/author', strict_slashes=False)
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
