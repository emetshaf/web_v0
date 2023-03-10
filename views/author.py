from flask import render_template, redirect
import requests
from uuid import uuid4
from web.config import api_status, get_username
from web.views import app_views


@ app_views.route('/author', strict_slashes=False)
def author():
    """Author Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        return redirect('/discover')
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)


@ app_views.route('/author/<author_id>', strict_slashes=False)
def get_author(author_id):
    """Author Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/authors/" + author_id
        books = requests.get("http://localhost/api/v1/books/").json()
        author = requests.get(url).json()
        return render_template(
            'author.html',
            author=author,
            books=books,
            username=get_username(),
            cache_id=cache_id,
        )
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)
