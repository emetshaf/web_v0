from flask import render_template, redirect
import requests
from uuid import uuid4
from web.views.common import api_status, get_username
from web.views import app_views


@app_views.route('/read/<book_id>', strict_slashes=False)
def read(book_id):
    """Read Page
    """
    if api_status()['status'] == 'OK':
        cache_id = uuid4()
        url = "http://localhost/api/v1/books/" + book_id
        book = requests.get(url).json()
        filename = book.get('file')
        extension = filename.split('.')[-1]
        return render_template(
            'read.html',
            book=book,
            extension=extension,
            username=get_username(),
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )
