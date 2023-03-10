from flask import render_template, request, redirect
import json
import os
import requests
from uuid import uuid4
from web.views.admin import admin_views
from web.config import api_status, allowed_file, UPLOAD_FOLDER, get_username


@ admin_views.route('/authors', strict_slashes=False)
def admin_authors():
    """Admin Authors Management Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        if get_username() is None:
            return redirect('/admin/signin')
        url = "http://localhost/api/v1/authors"
        authors = requests.get(url).json()
        return render_template(
            'admin/authors.html',
            authors=authors,
            segment='authors',
            cache_id=cache_id,
        )
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)


@admin_views.route('/edit_author/<author_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_author(author_id):
    """Admin Edit Author Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/authors/" + author_id
        author = requests.get(url).json()
        if request.method == 'POST':
            url = "http://localhost/api/v1/authors/" + author_id
            filename = ''
            if 'file' in request.files:
                file = request.files['file']
                if file and allowed_file(file.filename):
                    extension = os.path.splitext(file.filename)[1]
                    filename = str(uuid4()) + extension
                    file.save(os.path.join(
                        UPLOAD_FOLDER + '/authors', filename))
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
            return redirect('/admin/authors')
        return render_template(
            'admin/edit_author.html',
            author=author,
            cache_id=cache_id,
        )
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)


@ admin_views.route('/create_author', methods=['POST'], strict_slashes=False)
def create_author():
    if request.method == 'POST':
        url = "http://localhost/api/v1/authors/"
        filename = ''
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                extension = os.path.splitext(file.filename)[1]
                filename = str(uuid4()) + extension
                file.save(os.path.join(
                    UPLOAD_FOLDER + '/authors', filename))
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
        return redirect('/admin/authors')


@ admin_views.route('/delete_author/<author_id>', strict_slashes=False)
def delete_author(author_id):
    url = "http://localhost/api/v1/authors/" + author_id
    requests.delete(url)
    return redirect('/admin/authors')
