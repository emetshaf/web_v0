from flask import render_template, request, redirect, make_response
import requests
from uuid import uuid4
from web.views.common import api_status, get_username
from web.views import app_views


@ app_views.route('/discover', strict_slashes=False)
def discover():
    """Discover Page
    """
    if api_status()['status'] == 'OK':
        access_token = request.cookies.get('access_token')
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
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )
