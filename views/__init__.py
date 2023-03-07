from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/')

from web.views.index import *
from web.views.auth import *
from web.views.about import *
from web.views.contact import *
from web.views.discover import *
from web.views.library import *
from web.views.book import *
from web.views.author import *
from web.views.read import *