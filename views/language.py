from flask import render_template, redirect
import requests
from uuid import uuid4
from web.config import api_status, get_username
from web.views import app_views


@ app_views.route('/language', strict_slashes=False)
def language():
    """Language Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        return redirect('/discover')
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)


@ app_views.route('/language/<language_id>', strict_slashes=False)
def get_language(language_id):
    """Author Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/languages/" + language_id
        books = requests.get("http://localhost/api/v1/books/").json()
        language = requests.get(url).json()
        return render_template(
            'language.html',
            language=language,
            books=books,
            username=get_username(),
            cache_id=cache_id,
        )
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)
