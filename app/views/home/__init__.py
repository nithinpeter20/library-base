from flask import Blueprint

home = Blueprint('home', __name__)

# Local imports
from . import home_views