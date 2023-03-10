from web.config import api_status
from flask import render_template, request, make_response, redirect
import requests
from uuid import uuid4
from web.views.admin import admin_views


@admin_views.route('/', methods=['GET'], strict_slashes=False)
def dashboard():
    """ Index page """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        access_token = request.cookies.get('access_token')
        if access_token != None:
            res = requests.get(
                'http://localhost/auth/status',
                headers={
                    'Authorization': 'access_token {}'.format(
                        access_token)
                }
            )
            res_data = res.json()
            if res_data.get('error'):
                response = make_response(redirect('/signin'))
                response.set_cookie('access_token', '', expires=0)
                return response
            data = res_data.get('data')
            username = data['username']
            url = 'http://localhost/api/v1/stats'
            response = requests.get(url).json()
            audiobooks = response['audiobooks']
            authors = response['authors']
            books = response['books']
            categories = response['categories']
            feedbacks = response['feedbacks']
            languages = response['languages']
            narrators = response['narrators']
            reviews = response['reviews']
            users = response['users']
            response = make_response(render_template(
                'admin/index.html',
                audiobooks=audiobooks,
                authors=authors,
                books=books,
                categories=categories,
                feedbacks=feedbacks,
                languages=languages,
                narrators=narrators,
                reviews=reviews,
                users=users,
                username=username,
                segment='dashboard',
                cache_id=cache_id,
            ))
            return response
        else:
            return redirect('/admin/signin')
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)
