from flask import render_template, redirect
import requests
from uuid import uuid4
from web.config import api_status, get_username
from web.views import app_views


@app_views.route('/read/<book_id>', strict_slashes=False)
def read(book_id):
    """Read Page
    """
    if api_status()['status'] == 'OK':
        if get_username() is None:
            return redirect('/signin')
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
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)
