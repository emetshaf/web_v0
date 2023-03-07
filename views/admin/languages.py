from flask import render_template, request, redirect
import json
import os
import requests
from uuid import uuid4
from web.views.admin import admin_views
from web.views.common import api_status, allowed_file, UPLOAD_FOLDER, get_username


@ admin_views.route('/languages', strict_slashes=False)
def admin_languages():
    """Admin Languages Management Page
    """
    if api_status()['status'] == 'OK':
        if get_username() is None:
            return redirect('/admin/signin')
        url = "http://localhost/api/v1/languages"
        languages = requests.get(url).json()
        cache_id = uuid4()
        return render_template(
            'admin/languages.html',
            languages=languages,
            segment='languages',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@admin_views.route('/edit_language/<language_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_language(language_id):
    """Admin Edit Language Page
    """
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/languages/" + language_id
        language = requests.get(url).json()
        if request.method == 'POST':
            name = request.form['name']
            payload = {
                'name': name
            }
            requests.put(url, json=payload)
            return redirect('/admin/languages')
        cache_id = uuid4()
        return render_template(
            'admin/edit_language.html',
            language=language,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ admin_views.route('/create_language', methods=['POST'], strict_slashes=False)
def create_language():
    if request.method == 'POST':
        url = "http://localhost/api/v1/languages/"
        name = request.form['name']
        payload = {
            'name': name
        }
        requests.post(url, json=payload)
        return redirect('/admin/languages')


@ admin_views.route('/delete_language/<language_id>', strict_slashes=False)
def delete_language(language_id):
    url = "http://localhost/api/v1/languages/" + language_id
    requests.delete(url)
    return redirect('/admin/languages')
