from flask import render_template, request, redirect
from uuid import uuid4
from web.config import api_status, get_username
import requests
from web.views import app_views


@ app_views.route('/contact', methods=['GET'], strict_slashes=False)
def contact():
    """Contact Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        return render_template(
            'contact.html',
            username=get_username(),
            cache_id=cache_id,
        )
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)


@ app_views.route('/create_feedback', methods=['POST'], strict_slashes=False)
def create_ffeedback():
    """create a feedback
    """
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
        return redirect('/contact')
