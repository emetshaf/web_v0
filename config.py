import os
from flask import request, make_response, redirect
import requests


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = APP_ROOT + '/static/uploads'

ALLOWED_EXTENSIONS = set(
    ['txt', 'webp', 'epub', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'oog', 'wma'])


def get_username():
    access_token = request.cookies.get('access_token')
    if access_token != None:
        headers = {'Authorization': 'access_token {}'.format(
            access_token)}
        res = requests.get(
            "http://localhost/auth/status",
            headers=headers)
        res_data = res.json()
        data = res_data.get('data')
        return data['username']
    else:
        return None


def api_status():
    """Checks status of api

    Returns:
        json: Ok / FAIL
    """
    url = 'http://0.0.0.0/api/v1/status'
    try:
        r = requests.get(url)
        return r.json()
    except Exception:
        return {'status': 'FAIL'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS
