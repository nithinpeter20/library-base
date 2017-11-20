# Views for admin blueprint
"""
admin/views.py
~~~~~~~~~~~~~~
Script for admin view
"""

#### Libraries
# Standard library
import os

# Local imports
from . import admin 
from .admin_forms import CreateBookForm
from .admin_forms import AddAuthorForm
from ...models import Books, Authors, BookPhotos
from ...models import LendRequest, ReturnRequest, Users, BookReview
from app import db

# Third-party libraries
from flask import render_template
from flask import request
from flask import flash
from flask import abort
from flask import redirect
from flask import url_for
from flask import send_from_directory
from flask.views import View
from flask_login import current_user
from flask_login import login_required,login_user, logout_user
from flask.views import MethodView
from werkzeug.utils import secure_filename
from sqlalchemy import or_

class AdminPage(View):
    """
    To render admin-books html page
    """
    def dispatch_request(self):
        """
        To render admin-books html page
        """
        if not current_user.is_admin:
            abort(403)

        return render_template('admin-base.html', title='Admin')

admin.add_url_rule('/', view_func=AdminPage.as_view('adminpage'))


class AdminBooks(View):
    """
    Displays the books in database
    """
    methods = ['GET', 'POST']

    def dispatch_request(self):
        """
        """
        books = Books.query.all()
        bookphotos = BookPhotos.query.all()

        if request.method == 'POST':
        
            """
            To add the book, ie render createbook form html
            """
            form = CreateBookForm()
      
            if form.validate_on_submit():
            
                image = request.files['image']
                filename = secure_filename(image.filename)
                image.save(os.path.join('media/images/books', filename))

                book = Books(name=form.name.data,
                             author_id = request.form.get('author'),
                             publication_date=form.publication_date.data,
                             rating=form.rating.data,
                             book_count=form.book_count.data)


                db.session.add(book)
                db.session.commit()

                bookphotos =BookPhotos(image_name=book.name,
                                       path=filename,
                                       book_id=book.book_id)
           
                db.session.add(bookphotos) 
                db.session.commit()

                flash('Successfully added book...:')
        
            return render_template('admin/admin-createbook.html', form=form, title='Create Book')

        return render_template('admin/admin-books.html', books=books, bookphotos=bookphotos)

admin.add_url_rule('/admin-books', 
                    view_func=AdminBooks.as_view('admin_books'), 
                    methods=['GET','POST'])

admin.add_url_rule('/admin-books/create-booksss', 
                    view_func=AdminBooks.as_view('create_book'), 
                    methods=['POST'])



@admin.route('/admin-books/<filename>')
@login_required
def get_book(filename):
    """
    Function to return book image from books directory
    """

    return send_from_directory(os.path.realpath('media/images/books'), filename)

class BookDetails(View):
    """
    Display all the book details 
    """
    def dispatch_request(self,book_id):
        """
        Book details of corresponding book
        """
        book = Books.query.get(book_id)
        book_review = BookReview.query.all()
        authors = Authors.query.all()

        return render_template('admin/admin-book-details.html', 
                                book=book, book_id=book_id, 
                                book_review=book_review,
                                authors=authors)
        
admin.add_url_rule('/admin-books/book-details/<int:book_id>', 
                    view_func=BookDetails.as_view('book_details'), 
                    methods=['GET'])


class AdminAuthors(MethodView):
    """
    Class for authors
    """
    def get(self):
        """
        Display all authors
        """
        authors = Authors.query.all()
        return render_template('admin/admin-authors.html', authors=authors)

    def post(self):
        """
        Render create author html
        """
        form = AddAuthorForm()
    
        if form.validate_on_submit():
            image = request.files['image']
            filename = secure_filename(image.filename)
            image.save(os.path.join('media/images/authors', filename))
          
            author = Authors(author_name=form.author_name.data,
                             place= form.place.data,
                             date_of_birth=form.date_of_birth.data,
                             image=filename)

            db.session.add(author)
            db.session.commit()
            flash('Successfully added author...:')
        
        return render_template('admin/admin-createauthor.html', 
                                form=form, title='Create Author')

admin.add_url_rule('/admin-authors', 
                    view_func=AdminAuthors.as_view('admin_authors'), 
                    methods=['GET','POST']) 

admin.add_url_rule('/admin-authors/create_author', 
                    view_func=AdminAuthors.as_view('create_author'), 
                    methods=['POST','GET'])      
        

@admin.route('/admin-authors/<filename>')
@login_required
def send_author(filename):
    """
    Function to return author image from directory
    """
   
    return send_from_directory(os.path.realpath('media/images/authors'), filename)

class AdminLend(View):
    """
    Lend requests from users
    """
    def dispatch_request(self):
        """
        Display all the lend requests from user
        """
        lend = LendRequest.query.filter(or_(LendRequest.status=="pending" ,
                                            LendRequest.status=="Rejected"))
        
        books = Books.query.all()
        users = Users.query.all()

        return render_template('admin/admin-lend.html', lend=lend, books=books, users=users)

admin.add_url_rule('/lend-request', 
                    view_func=AdminLend.as_view('lend_request'), methods=['GET','POST']) 


@admin.route('/lend-request/lend-approve/<int:lend_id>', methods=['GET', 'POST'])
def lend_approve(lend_id):
    """
    To render admin-lend html page and update status to 'approved'
    """
    
    lend_object = LendRequest.query.get(lend_id)
    book_object = Books.query.get(lend_object.book_id)
    lend_object.status="Approved"      
    db.session.commit()
    lend = LendRequest.query.filter(or_(LendRequest.status=="pending" , 
                                        LendRequest.status=="Rejected"))
    books = Books.query.all()
    users = Users.query.all()

    return render_template('admin/admin-lend.html' , lend=lend, books=books, users=users)


@admin.route('/lend-request/lend-reject/<int:lend_id>', methods=['GET', 'POST'])
def lend_reject(lend_id):
    """
    To render admin-lend html page and update status to 'rejected'
    """

    lend_object = LendRequest.query.get(lend_id)
    lend_object.status = "Rejected"
    book_object = Books.query.get(lend_object.book_id)
    db.session.commit()
    lend = LendRequest.query.filter(or_(LendRequest.status=="pending" , 
                                        LendRequest.status=="Rejected"))
    users = Users.query.all()
    books = Books.query.all()

    return render_template('admin/admin-lend.html',lend=lend, books=books, users=users)



class AdminReturn(View):
    """
    Class for return requests from user
    """
    def dispatch_request(self):
        """
        Display all the return requests from user
        """
        rbooks = ReturnRequest.query.filter(or_(ReturnRequest.status=="pending" , 
                                                ReturnRequest.status=="Rejected"))
        users = Users.query.all()
        books = Books.query.all()

        return render_template('admin/admin-return.html',
                                rbooks=rbooks, users=users, books=books)

admin.add_url_rule('/return-request', 
                    view_func=AdminReturn.as_view('return_request'), 
                    methods=['GET','POST'])





@admin.route('/return-request/return-approve/<int:return_id>/<int:user_id>', 
              methods=['GET', 'POST'])

def return_approve(return_id,user_id):
    """
    To render admin-lend html page and update status to 'approved'
    """
    
    return_object = ReturnRequest.query.get(return_id)
    return_object.status = "Received"
    book_object = Books.query.get(return_object.book_id)
    book_object.book_count = book_object.book_count+1
    user = Users.query.get(user_id)
    user.card_count = user.card_count + 1
    db.session.commit()
    rbooks = ReturnRequest.query.filter(or_(ReturnRequest.status=="pending" , ReturnRequest.status=="Rejected"))
    books = Books.query.all()
    users = Users.query.all()

    return render_template('admin/admin-return.html' , rbooks=rbooks, books=books, users=users)



@admin.route('/return-request/return-reject/<int:return_id>', methods=['GET', 'POST'])
def return_reject(return_id):
    """
    To render admin-return-book html page and update status to 'rejected'
    """
    return_object = ReturnRequest.query.get(return_id)
    return_object.status = "Rejected"
    book_object = Books.query.get(return_object.book_id)
    db.session.commit()
    rbooks = ReturnRequest.query.filter(or_(ReturnRequest.status=="pending" , ReturnRequest.status=="Rejected"))
    books = Books.query.all()
    users = Users.query.all()
    return render_template('admin/admin-return.html',rbooks=rbooks, books=books, users=users)

