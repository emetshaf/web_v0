from flask import render_template, redirect
import requests
from uuid import uuid4
from web.views.common import api_status, get_username
from web.views import app_views


@ app_views.route('/book', strict_slashes=False)
def book():
    """Book Page
    """
    if api_status()['status'] == 'OK':
        cache_id = uuid4()
        return redirect('/discover')
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )
        

@ app_views.route('/book/<book_id>', strict_slashes=False)
def get_book(book_id):
    """Book Page
    """
    if api_status()['status'] == 'OK':
        cache_id = uuid4()
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
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )