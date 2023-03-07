from flask import render_template, request, redirect, make_response
import json
import requests
from uuid import uuid4
from web.views.admin import admin_views
from web.views.common import api_status


@admin_views.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def admin_signup():
    """Admin Signup Page
    """
    if api_status()['status'] == 'OK':
        access_token = request.cookies.get('access_token')
        if access_token != None:
            return redirect('/')
        url = "http://localhost/auth/signup"
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            payload = {
                'username': username,
                'password': password
            }
            requests.post(url, json=payload)
            return redirect('/admin/signin')
        cache_id = uuid4()
        return render_template(
            'admin/sign-up.html',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ admin_views.route('/signin', methods=['GET', 'POST'], strict_slashes=False)
def admin_signin():
    """Admin Signin Page
    """
    if api_status()['status'] == 'OK':
        access_token = request.cookies.get('access_token')
        if access_token != None:
            return redirect('/admin')
        url = "http://localhost/auth/signin"
        cache_id = uuid4()
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            payload = {
                'username': username,
                'password': password
            }
            log = requests.post(url, json=payload)
            if log.status_code == 200:
                auth_token = log.json()['auth_token']
                response = make_response(redirect('/admin'))
                response.set_cookie(
                    'access_token', auth_token, max_age=60*60*24)
                return response

        return render_template(
            'admin/sign-in.html',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@admin_views.route('/signout', methods=['GET'], strict_slashes=False)
def signout():
    """ Signout page """
    access_token = request.cookies.get('access_token')
    requests.post(
        "http://localhost/auth/signout",
        headers={'Authorization': 'access_token {}'.format(
            access_token)})
    response = make_response(redirect('/admin/signin'))
    response.set_cookie('access_token', '', expires=0)
    return response
