from flask import render_template
from uuid import uuid4
from web.views.common import api_status, get_username
from web.views import app_views


@app_views.route('/about', strict_slashes=False)
def about():
    """About Page
    """
    if api_status()['status'] == 'OK':
        cache_id = uuid4()
        return render_template(
            'about.html',
            username=get_username(),
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )
