from flask import render_template, request, redirect
import json
import os
import requests
from uuid import uuid4
from web.views.admin import admin_views
from web.views.common import api_status, allowed_file, UPLOAD_FOLDER, get_username


@ admin_views.route('/feedbacks', strict_slashes=False)
def admin_feedbacks():
    """Admin Feedback Management Page
    """
    if api_status()['status'] == 'OK':
        if get_username() is None:
            return redirect('/admin/signin')
        url = "http://localhost/api/v1/feedbacks"
        feedbacks = requests.get(url).json()
        cache_id = uuid4()
        return render_template(
            'admin/feedbacks.html',
            feedbacks=feedbacks,
            segment='feedbacks',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@admin_views.route('/edit_feedback/<feedback_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_feedback(feedback_id):
    """Admin Edit Feedback Page
    """
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/feedbacks/" + feedback_id
        feedback = requests.get(url).json()
        if request.method == 'POST':
            full_name = request.form['full_name']
            email = request.form['email']
            message = request.form['message']
            payload = {
                'full_name': full_name,
                'email': email,
                'message': message
            }
            requests.put(url, json=payload)
            return redirect('/admin/feedbacks')
        cache_id = uuid4()
        return render_template(
            'admin/edit_feedback.html',
            feedback=feedback,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ admin_views.route('/create_feedback', methods=['POST'], strict_slashes=False)
def create_feedback():
    if request.method == 'POST':
        url = "http://localhost/api/v1/feedbacks/"
        full_name = request.form['full_name']
        email = request.form['email']
        message = request.form['message']
        payload = {
            'full_name': full_name,
            'email': email,
            'message': message
        }
        requests.post(url, json=payload)
        return redirect('/admin/feedbacks')


@ admin_views.route('/delete_feedback/<feedback_id>', strict_slashes=False)
def delete_feedback(feedback_id):
    url = "http://localhost/api/v1/feedbacks/" + feedback_id
    requests.delete(url)
    return redirect('/admin/feedbacks')
