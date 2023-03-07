from flask import Blueprint
admin_views = Blueprint('admin_views', __name__, url_prefix='/admin')

from web.views.admin.index import *
from web.views.admin.auth import *
from web.views.admin.audiobooks import *
from web.views.admin.authors import *
from web.views.admin.books import *
from web.views.admin.categories import *
from web.views.admin.feedbacks import *
from web.views.admin.languages import *
from web.views.admin.narrators import *
from web.views.admin.reviews import *
from web.views.admin.users import *