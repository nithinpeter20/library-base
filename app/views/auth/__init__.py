from flask import Blueprint

auth = Blueprint('auth', __name__)

# Local imports
from . import auth_views