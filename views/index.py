from web.config import api_status, get_username
from flask import render_template, request, redirect, make_response
import requests
from uuid import uuid4
from web.views import app_views


@ app_views.route('/', methods=['GET'], strict_slashes=False)
def home():
    """Home Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        username = get_username()
        return render_template(
            'index.html',
            username=username,
            cache_id=cache_id,
        )
    else:
        return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)
