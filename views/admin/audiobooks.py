from flask import render_template, request, redirect
import json
import os
import requests
from uuid import uuid4
from web.views.admin import admin_views
from web.config import api_status, get_username, allowed_file, UPLOAD_FOLDER


@ admin_views.route('/audiobooks', strict_slashes=False)
def admin_audiobooks():
    """Admin AudioBooks Management Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        if get_username() is None:
            return redirect('/admin/signin')
        url = "http://localhost/api/v1/audiobooks"
        audiobooks = requests.get(url).json()
        books = requests.get("http://localhost/api/v1/books").json()
        narrators = requests.get("http://localhost/api/v1/narrators").json()
        return render_template(
            'admin/audiobooks.html',
            audiobooks=audiobooks,
            books=books,
            narrators=narrators,
            segment='audioboks',
            cache_id=cache_id,
        )
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)


@admin_views.route('/edit_audiobook/<audiobook_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_audiobook(audiobook_id):
    """Admin Edit AudioBooks Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/audiobooks/" + audiobook_id
        audiobook = requests.get(url).json()
        if request.method == 'POST':
            url = "http://localhost/api/v1/audiobooks/" + audiobook_id
            file = request.form['file']
            payload = {
                'file': file
            }
            requests.put(url, json=payload)
            return redirect('/admin/audiobooks')
        return render_template(
            'admin/edit_audiobook.html',
            audiobook=audiobook,
            cache_id=cache_id,
        )
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)


@ admin_views.route('/create_audiobook', methods=['POST'], strict_slashes=False)
def create_audiobook():
    if request.method == 'POST':
        book_id = request.form['book_id']
        title = requests.get("http://localhost/api/v1/books/" +
                             book_id).json().get('title')
        fold = title.replace(" ", "_")
        folder = os.path.join(UPLOAD_FOLDER +
                              '/audiobooks/' + fold + '/')
        if not os.path.exists(folder):
            os.mkdir(folder)
        url = "http://localhost/api/v1/audiobooks/"
        file = request.files['file']
        narrator_id = request.form['narrator_id']
        narrator = requests.get(
            "http://localhost/api/v1/narrators/" + narrator_id).json()
        narrator_name = narrator.get(
            'first_name') + narrator.get('middle_name') + narrator.get('last_name')
        filename = ''
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                extension = os.path.splitext(file.filename)[1]
                filename = narrator_name + extension
                file.save(os.path.join(
                    folder + filename))
                file = filename
        payload = {
            'file': fold + '/' + filename,
            'book_id': book_id,
            'narrator_id': narrator_id
        }
        requests.post(url, json=payload)
        return redirect('/admin/audiobooks')


@ admin_views.route('/delete_audiobook/<audiobook_id>', strict_slashes=False)
def delete_audiobook(audiobook_id):
    url = "http://localhost/api/v1/audiobooks/" + audiobook_id
    requests.delete(url)
    return redirect('/admin/audiobooks')
