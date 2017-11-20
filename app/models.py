# app/models.py
"""
A script to create models 
"""

#### Libraries
# Standard library

# Third-party libraries
import urllib.request
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask.ext.bcrypt import Bcrypt
from alembic import op

# Local imports
from app import db
from app import login_manager

# Object to encrypt and decrypt password
bcrypt = Bcrypt()

class Users(UserMixin, db.Model):
    """
    This create a User Table which contain list of registered users
    """
    __tablename__ = 'Users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True)
    username = db.Column(db.String(60), index=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    card_count = db.Column(db.Integer, default=5)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    l_request = db.relationship('LendRequest', backref='User-Lend_Request', lazy='dynamic')
    r_request = db.relationship('ReturnRequest', backref='User-Return_Request', lazy='dynamic')
    review = db.relationship('BookReview', backref='User-Book-review', lazy='dynamic')
    
    @property
    def password(self):
        """
        prevent password being accessed
        """
        raise AttributeError('password is not readable')
        return self. password

    @password.setter
    def password(self, password):
        """
        Set password to hashed password
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Check if password matches
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Users: {}>'.format(self.username)


#Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    """
    Function to load user
    """

    return Users.query.get(int(user_id))


class BookPhotos(db.Model):
    """
    Create Photos table
    """

    __tablename__ = "Book_Photos"
    image_id = db.Column(db.Integer, primary_key=True)
    image_name =  db.Column(db.String(60), index=True)
    path = db.Column(db.String, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('Books.book_id'))

    def __repr__(self):
        return '<BookPhotos: {}>'.format(self.image_name)

class Books(db.Model):
    """
    Create Books table
    """

    __tablename__ = "Books"
    book_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('Authors.author_id'))
    publication_date = db.Column(db.Date, index=True)
    rating = db.Column(db.Float, index=True)
    book_count = db.Column(db.Integer, index=True)
    image = db.relationship('BookPhotos', backref='Book_Photos',lazy='dynamic')
    l_request = db.relationship('LendRequest', backref='Book-Lend_Request', lazy='dynamic')
    r_request = db.relationship('ReturnRequest', backref='Book-Return_Request', lazy='dynamic')
    review = db.relationship('BookReview', backref='Book-Review', lazy='dynamic')
    
    

    def __repr__(self):
        return '<Books: {}>'.format(self.name)    



class Authors(db.Model):
    """
    Create authors table
    """

    __tablename__ = "Authors"
    author_id = db.Column(db.Integer, primary_key=True)
    author_name =  db.Column(db.String(60), index=True)
    place =  db.Column(db.String(60), index=True)    
    date_of_birth = db.Column(db.Date, index=True)
    image = db.Column(db.String, index=True)
    book_reln = db.relationship('Books', backref='book', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.author_name)


class LendRequest(db.Model):
    """
    Create Lend Request table
    """

    __tablename__ = "Lend_Request"
    lend_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    book_id =  db.Column(db.Integer, db.ForeignKey('Books.book_id'))
    date =  db.Column(db.Date, index=True)
    status = db.Column(db.String(60), index=True)
    r_request = db.relationship('ReturnRequest', backref='Books-Return_Request', lazy='dynamic')



    def __repr__(self):
        return '<LendRequest: {}>'.format(self.user_id)


class ReturnRequest(db.Model):
    """
    Create return request table
    """

    __tablename__ = "Return_Request"
    return_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    book_id =  db.Column(db.Integer, db.ForeignKey('Books.book_id'))
    date =  db.Column(db.Date, index=True)
    status = db.Column(db.String(60), index=True)
    lend_id = db.Column(db.Integer, db.ForeignKey('Lend_Request.lend_id'))



    def __repr__(self):
        return '<ReturnRequest: {}>'.format(self.user_id)

class BookReview(db.Model):
    """
    Create return request table
    """
    __tablename__ = "Book_Review"
    review_id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(200), index=True)
    book_id =  db.Column(db.Integer, db.ForeignKey('Books.book_id'))
    user_id =  db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return '<BookReview: {}>'.format(self.review_id)



