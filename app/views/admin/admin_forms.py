# Forms for admin blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextField, DateField, FloatField, IntegerField,  ValidationError
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from ...models import Authors
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField


class CreateBookForm(FlaskForm):
	"""
	Form for creating book
	"""

	name = StringField('Book Name', validators=[DataRequired()])	
	author = QuerySelectField(query_factory=lambda: Authors.query.all())
	publication_date = DateField('Publication_date', format='%Y-%m-%d')
	rating = FloatField("Rating", validators=[DataRequired()])
	book_count = IntegerField('Count', validators= [DataRequired()])
	image = FileField('image', validators=[FileRequired()])
	submit = SubmitField('Create Book')


class AddAuthorForm(FlaskForm):
	"""
	Form for adding author
	"""

	author_name = StringField('Author Name', validators=[DataRequired()])
	place = StringField('Place', validators=[DataRequired()])
	date_of_birth = DateField('DOB', format='%Y-%m-%d')
	image = FileField('image', validators=[FileRequired()])
	submit = SubmitField('Add Author')
