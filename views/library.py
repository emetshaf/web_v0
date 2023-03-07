from flask import render_template, request, redirect, make_response
import requests
from uuid import uuid4
from web.views.common import api_status
from web.views import app_views


@ app_views.route('/library', strict_slashes=False)
def library():
    """Library Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        access_token = request.cookies.get('access_token')
        if access_token != None:
            url = 'http://localhost/auth/status'
            headers = {'Authorization': 'access_token {}'.format(
                access_token)}
            res = requests.get(
                "http://localhost/auth/status",
                headers=headers)
            res_data = res.json()
            if res_data.get('error'):
                response = make_response(redirect('/signin'))
                response.set_cookie('access_token', '', expires=0)
                return response
            data = res_data.get('data')
            username = data['username']
            response = make_response(render_template(
                'library.html',
                username=username,
                cache_id=cache_id,
            ))
            return response
        else:
            return redirect('/signin')
    else:
        return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)
