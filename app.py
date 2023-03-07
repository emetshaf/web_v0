from web.views import app_views
from web.views.admin import admin_views
from flask import Flask, make_response, render_template, url_for, request
import os
import requests
from uuid import uuid4
import logging


logging.basicConfig(level=logging.DEBUG, filename='web.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = APP_ROOT + '/static/uploads'
ALLOWED_EXTENSIONS = set(
    ['txt', 'webp', 'epub', 'png',
     'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'oog', 'wma'])


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

app.register_blueprint(app_views)
app.register_blueprint(admin_views)


@app.errorhandler(404)
def not_found(error):
    cache_id = uuid4()
    return render_template('error.html', error_code='404',
                           message='Page Not Found', cache_id=cache_id)


@app.errorhandler(500)
def internal_error(error):
    cache_id = uuid4()
    return render_template('error.html', error_code='500',
                           message='Internal Server Error', cache_id=cache_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
