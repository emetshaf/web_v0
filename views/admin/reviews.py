from flask import render_template, request, redirect
import json
import os
import requests
from uuid import uuid4
from web.views.admin import admin_views
from web.views.common import api_status, allowed_file, UPLOAD_FOLDER, get_username


@ admin_views.route('/reviews', strict_slashes=False)
def admin_reviews():
    """Admin Reviews Management Page
    """
    if api_status()['status'] == 'OK':
        if get_username() is None:
            return redirect('/admin/signin')
        url = "http://localhost/api/v1/reviews"
        reviews = requests.get(url).json()
        users = requests.get("http://localhost/api/v1/users").json()
        books = requests.get("http://localhost/api/v1/books").json()
        cache_id = uuid4()
        return render_template(
            'admin/reviews.html',
            reviews=reviews,
            users=users,
            books=books,
            segment='reviews',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ admin_views.route('/create_review', methods=['POST'], strict_slashes=False)
def create_review():
    if request.method == 'POST':
        url = "http://localhost/api/v1/reviews/"
        text = request.form['text']
        user_id = request.form['user']
        book_id = request.form['book']
        payload = {
            'text': text,
            'user_id': user_id,
            'book_id': book_id
        }
        requests.post(url, json=payload)
        return redirect('/admin/reviews')


@ admin_views.route('/delete_review/<review_id>', strict_slashes=False)
def delete_review(review_id):
    url = "http://localhost/api/v1/reviews/" + review_id
    requests.delete(url)
    return redirect('/admin/reviews')
