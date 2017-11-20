# Forms for admin blueprint
from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms import SubmitField, SelectField
from wtforms import TextField, DateField
from wtforms import FloatField, IntegerField, ValidationError
from wtforms.validators import DataRequired
from wtforms import TextAreaField


class LendRequestForm(FlaskForm):
	"""
	Form for lending request
	"""

	user_id = IntegerField('User id', validators=[DataRequired()])
	book_id =IntegerField('Book id', validators=[DataRequired()])
	date = DateField('Date',  format='%m/%d/%Y')
	status = StringField('status', validators=[DataRequired()])
	submit = SubmitField('Lend Book')


class ReturnRequestForm(FlaskForm):
	"""
	Form for return request
	"""

	user_id = IntegerField('User id', validators=[DataRequired()])
	book_id =IntegerField('Boook id', validators=[DataRequired()])
	date = DateField('Date', validators= [DataRequired()])
	status = StringField('status', validators=[DataRequired()])
	submit = SubmitField('Return Book')


class WriteReview(FlaskForm):
	"""
	Form for return request
	"""

	review = TextAreaField('Review', validators=[DataRequired()])
	submit = SubmitField('Submit Review')