from flask import render_template, request
import requests
from uuid import uuid4
from web.config import api_status, get_username
from web.views import app_views


@ app_views.route('/discover', strict_slashes=False)
def discover():
    """Discover Page
    """
    if api_status()['status'] == 'OK':
        username = get_username()
        cache_id = uuid4()
        url = "http://localhost/api/v1/books"
        books = requests.get(url).json()
        return render_template(
            'discover.html',
            books=books,
            username=username,
            cache_id=cache_id,
        )
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)
