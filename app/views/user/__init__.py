from flask import Blueprint

user = Blueprint('user', __name__)

# Local imports
from . import user_views