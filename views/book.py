from flask import render_template, redirect
import requests
from uuid import uuid4
from web.config import api_status, get_username
from web.views import app_views


@ app_views.route('/book', strict_slashes=False)
def book():
    """Book Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        return redirect('/discover')
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)


@ app_views.route('/book/<book_id>', strict_slashes=False)
def get_book(book_id):
    """Book Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/books/" + book_id
        book = requests.get(url).json()
        authors = requests.get("http://localhost/api/v1/authors").json()
        return render_template(
            'book.html',
            book=book,
            authors=authors,
            username=get_username(),
            cache_id=cache_id,
        )
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)
