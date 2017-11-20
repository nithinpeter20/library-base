from flask import Blueprint

admin = Blueprint('admin', __name__)

# Local imports
from . import admin_views