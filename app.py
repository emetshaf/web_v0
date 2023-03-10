from web.views import app_views
from web.views.admin import admin_views
from flask import Flask, make_response, render_template, url_for, request
import os
import requests
from uuid import uuid4
import logging
from web.config import APP_ROOT, UPLOAD_FOLDER, ALLOWED_EXTENSIONS


logging.basicConfig(level=logging.DEBUG, filename='web.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

app.register_blueprint(app_views)
app.register_blueprint(admin_views)


@app.errorhandler(404)
def not_found(error):
    cache_id = uuid4()
    error.message = 'Page not found'
    return render_template('error.html', error_code=error.code,
                           message=error.message, cache_id=cache_id)


@app.errorhandler(500)
def internal_error(error):
    cache_id = uuid4()
    error.message = 'Internal Server Error'
    return render_template('error.html', error_code=error.code,
                           message=error.message, cache_id=cache_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
