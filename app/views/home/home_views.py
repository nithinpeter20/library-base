# app/home/views.py
"""
Views for homepage
"""
### Libraries
# Third party libraries
from flask_login import login_required
from flask_login import current_user
from flask import render_template
from flask.views import View

# Local imports
from . import home

class Home(View):
	"""
	Renders the homepage
	"""
	def dispatch_request(self):
		"""
		Homepage get rendered 
		"""
		return render_template('home.html', title="Home")

home.add_url_rule('/', view_func=Home.as_view('home'))


