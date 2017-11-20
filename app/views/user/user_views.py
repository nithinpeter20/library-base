
#app/auth/views.py
"""
Views for authentication of users
"""
### Libraries
# Standard library
import os
import datetime

# Third party libraries
from flask import render_template
from flask import request
from flask import flash
from flask import abort
from flask import redirect
from flask import url_for
from flask import send_from_directory
from flask_login import current_user
from flask_login import login_required,login_user, logout_user
from flask.views import View,MethodView
from sqlalchemy import or_

# Local imports
from app import db
from .user_forms import LendRequestForm, WriteReview
from . import user
from ...models import Users,Authors
from ...models import Books,BookPhotos,LendRequest,ReturnRequest,Users,BookReview


class UserPage(View):
    """
    Class for rendering userpage
    """
    def dispatch_request(self):
        """
        Call user-base.html page for rendering user base page
        """
        return render_template('user-base.html', title='Admin')

user.add_url_rule('/', view_func=UserPage.as_view('userpage'))




class UserBooks(MethodView):
    """
    Class for rendering Books for user
    """

    def get(self):
        """
        Display all the books
        """

        books = Books.query.all()
        bookphotos = BookPhotos.query.all()
        
        return render_template('user/user-books.html', books=books, bookphotos=bookphotos)


user.add_url_rule('/user-books', view_func=UserBooks.as_view('user_books'))


class BookDetails(View):
    """
    Class for displaying book details
    """
    def dispatch_request(self,book_id):
        """
        Display all book details
        """
        book = Books.query.get(book_id)
        book_review = BookReview.query.all()
        authors = Authors.query.all()

        return render_template('book-details.html', book=book, 
                                book_id=book_id, book_review=book_review,
                                authors=authors)
        
user.add_url_rule('/user-books/book-details/<int:book_id>', 
                  view_func=BookDetails.as_view('book_details'), methods=['GET'])



@user.route('/book-details/<int:book_id>')
def send_book(book_id):
    """
	To get image of selected book only
    """
    bookphotos_object = BookPhotos.query.get(book_id)
    book_image = send_from_directory(os.path.realpath('media/images/books'), 
                                     bookphotos_object.path)

    return book_image



class LendForm(View):
    """
    Class for requesting the book
    """
    def dispatch_request(self,book_id,userid):
        """
        Book get requested
        """
        book = Books.query.get(book_id)
        print ("Book count.................",book.book_count)

        user = Users.query.get(userid)
            
        if book.book_count > 0 and user.card_count > 0:

            lend = LendRequest(user_id=userid,
                               book_id= book_id,
                               date=datetime.date.today(),
                               status= "pending")

            book.book_count = book.book_count - 1
            user.card_count = user.card_count - 1

            db.session.add(lend)
            db.session.commit()
            flash('Successfully requested book...:')
    
        elif book.book_count == 0 :
            flash('Book count is 0 ...Cant borrow:')

        else :
            flash('Your card limit over...Cant borrow:')   

        book_review = BookReview.query.all()
    
        return render_template('book-details.html', book=book, book_id=book_id, book_review=book_review)
        
user.add_url_rule('/book-details/lend-request/<int:userid>/<int:book_id>', 
                  view_func=LendForm.as_view('lend_form'), methods=['GET'])



class LendRequests(View):
    """
    Lend requests of corresponding user
    """
    def dispatch_request(self,user_id):
        """
        Display all the lend requests of corresponding user
        """
        lend = LendRequest.query.filter(LendRequest.user_id==user_id, 
                                        or_(LendRequest.status=="pending", 
                                        LendRequest.status=="Rejected") )
        books = Books.query.all()
        users = Users.query.all()

        return render_template('user/user-lendrequest.html', 
                                lend=lend, books=books, users=users)
        
user.add_url_rule('/lend-request/<int:user_id>', 
                  view_func=LendRequests.as_view('lend_request'), methods=['GET'])



class BorrowedBooks(View):
    """
    Borrowed books of corresponding user
    """
    def dispatch_request(self,user_id):
        """
        Display all the borrowed books of corresponding user
        """
        lend = LendRequest.query.filter(LendRequest.user_id==user_id, 
                                        LendRequest.status=="Approved" )

        users = Users.query.all()
        books = Books.query.all()

        

        return render_template('user/borrowed-books.html', lend=lend, 
                                users=users, books=books)
        
user.add_url_rule('/borrowed-books/<int:user_id>', 
                  view_func=BorrowedBooks.as_view('borrowed_books'), methods=['GET'])




@user.route('/returned-books/<int:lend_id>/<int:user_id>/<int:book_id>/', methods=['GET', 'POST'])
@login_required
def returned_books(lend_id,user_id,book_id):
    """
    Function to return book . ie, book return button redirects to this
    """

    ret_book = ReturnRequest(user_id=user_id,
                             book_id= book_id,
                             date=datetime.date.today(),
                             status= "pending",
                             lend_id=lend_id)
    
    lend_object = LendRequest.query.get(lend_id)
    lend_object.status = "Returned"

    db.session.add(ret_book)
    db.session.commit()
    lend = LendRequest.query.filter(LendRequest.user_id==user_id, 
                                    LendRequest.status=="Approved" )

    users = Users.query.all()
    books = Books.query.all()
    #return "returned_books"
    return render_template('user/borrowed-books.html', lend=lend,
                            users=users, books=books)




class BooksReturned(View):
    """
    Returned books of corresponding user
    """
    def dispatch_request(self):
        """
        Display all the returned books of corresponding user
        """
        rbooks = ReturnRequest.query.all()  
        users = Users.query.all()
        books = Books.query.all()
        return render_template('user/returned-books.html', 
                                rbooks=rbooks, users=users, books=books)
        
user.add_url_rule('/books-returned',
                  view_func=BooksReturned.as_view('books_returned'), methods=['GET'])




class BooksReviews(View):
    """
    Write review for received book
    """
    def dispatch_request(self,return_id,user_id,book_id):
        """
        Write review for received book
        """
        users = Users.query.all()
        books = Books.query.all()
        form = WriteReview()


        if  not form.validate_on_submit():
            review = BookReview(review=form.review.data,
                            book_id=book_id,
                            user_id=user_id)
       
            db.session.add(review)
            db.session.commit()

        return render_template('user/review.html',users=users, books=books, form=form)

user.add_url_rule('/book-review/<int:return_id>/<int:user_id>/<int:book_id>/', 
                  view_func=BooksReviews.as_view('book_review'), methods=['GET','POST'])


