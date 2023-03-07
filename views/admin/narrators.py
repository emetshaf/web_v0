from flask import render_template, request, redirect
import json
import os
import requests
from uuid import uuid4
from web.views.admin import admin_views
from web.views.common import api_status, allowed_file, UPLOAD_FOLDER, get_username


@ admin_views.route('/narrators', strict_slashes=False)
def admin_narrators():
    """Admin Narrators Management Page
    """
    if api_status()['status'] == 'OK':
        if get_username() is None:
            return redirect('/admin/signin')
        url = "http://localhost/api/v1/narrators"
        narrators = requests.get(url).json()
        cache_id = uuid4()
        return render_template(
            'admin/narrators.html',
            narrators=narrators,
            segment='narrators',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@admin_views.route('/edit_narrator/<narrator_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_narrator(narrator_id):
    """Admin Edit Narrator Page
    """
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/narrators/" + narrator_id
        narrator = requests.get(url).json()
        if request.method == 'POST':
            filename = ''
            if 'file' in request.files:
                file = request.files['file']
                if file and allowed_file(file.filename):
                    extension = os.path.splitext(file.filename)[1]
                    filename = str(uuid4()) + extension
                    file.save(os.path.join(
                        UPLOAD_FOLDER + '/narrators', filename))
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['last_name']
            if filename == '':
                payload = {
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'last_name': last_name
                }
            else:
                payload = {
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'last_name': last_name,
                    'image': filename
                }
            requests.put(url, json=payload)
            return redirect('/admin/narrators')
        cache_id = uuid4()
        return render_template(
            'admin/edit_narrator.html',
            narrator=narrator,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ admin_views.route('/create_narrator', methods=['POST'], strict_slashes=False)
def create_narrator():
    if request.method == 'POST':
        url = "http://localhost/api/v1/narrators/"
        filename = ''
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                extension = os.path.splitext(file.filename)[1]
                filename = str(uuid4()) + extension
                file.save(os.path.join(
                    UPLOAD_FOLDER + '/narrators', filename))
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        payload = {
            'image': filename,
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name
        }
        requests.post(url, json=payload)
        return redirect('/admin/narrators')


@ admin_views.route('/delete_narrator/<narrator_id>', strict_slashes=False)
def delete_narrator(narrator_id):
    url = "http://localhost/api/v1/narrators/" + narrator_id
    requests.delete(url)
    return redirect('/admin/narrators')
