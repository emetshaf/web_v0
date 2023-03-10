from flask import render_template
from uuid import uuid4
from web.config import api_status, get_username
from web.views import app_views


@app_views.route('/about', strict_slashes=False)
def about():
    """About Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        return render_template(
            'about.html',
            username=get_username(),
            cache_id=cache_id,
        )
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)
