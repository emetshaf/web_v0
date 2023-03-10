from flask import render_template, request, redirect
import json
import os
import requests
from uuid import uuid4
from web.views.admin import admin_views
from web.config import api_status, allowed_file, UPLOAD_FOLDER, get_username


@ admin_views.route('/users', strict_slashes=False)
def admin_users():
    """Admin Users Management Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        if get_username() is None:
            return redirect('/admin/signin')
        url = "http://localhost/api/v1/users"
        users = requests.get(url).json()
        return render_template(
            'admin/users.html',
            users=users,
            segment='users',
            cache_id=cache_id,
        )
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)


@admin_views.route('/edit_user/<user_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_user(user_id):
    """Edit User Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/users/" + user_id
        user = requests.get(url).json()
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if password == '':
                payload = {
                    'username': username
                }
            else:
                payload = {
                    'username': username,
                    'password': password
                }
            requests.put(url, json=payload)
            return redirect('/admin/users')
        return render_template(
            'admin/edit_user.html',
            user=user,
            cache_id=cache_id,
        )
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)


@ admin_views.route('/create_user', methods=['POST'], strict_slashes=False)
def create_user():
    if request.method == 'POST':
        url = "http://localhost/api/v1/users/"
        username = request.form['username']
        password = request.form['password']
        payload = {
            'username': username,
            'password': password
        }
        requests.post(url, json=payload)
        return redirect('/admin/users')


@ admin_views.route('/delete_user/<user_id>', strict_slashes=False)
def delete_user(user_id):
    url = "http://localhost/api/v1/users/" + user_id
    requests.delete(url)
    return redirect('/admin/users')
