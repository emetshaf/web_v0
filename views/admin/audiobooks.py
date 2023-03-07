from flask import render_template, request, redirect
import json
import requests
from uuid import uuid4
from web.views.admin import admin_views
from web.views.common import api_status, get_username


@ admin_views.route('/audiobooks', strict_slashes=False)
def admin_audiobooks():
    """Admin AudioBooks Management Page
    """
    if api_status()['status'] == 'OK':
        if get_username() is None:
            return redirect('/admin/signin')
        url = "http://localhost/api/v1/audiobooks"
        audiobooks = requests.get(url).json()
        cache_id = uuid4()
        return render_template(
            'admin/audiobooks.html',
            audiobooks=audiobooks,
            segment='audioboks',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@admin_views.route('/edit_audiobook/<audiobook_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_audiobook(audiobook_id):
    """Admin Edit AudioBooks Page
    """
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
        cache_id = uuid4()
        return render_template(
            'admin/edit_audiobook.html',
            audiobook=audiobook,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ admin_views.route('/create_audiobook', methods=['POST'], strict_slashes=False)
def create_audiobook():
    if request.method == 'POST':
        url = "http://localhost/api/v1/audiobooks/"
        file = request.form['file']
        payload = {'file': file}
        requests.post(url, json=payload)
        return redirect('/admin/audiobooks')


@ admin_views.route('/delete_audiobook/<audiobook_id>', strict_slashes=False)
def delete_audiobook(audiobook_id):
    url = "http://localhost/api/v1/audiobooks/" + audiobook_id
    requests.delete(url)
    return redirect('/admin/audiobooks')
