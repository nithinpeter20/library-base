#app/auth/views.py
"""
Views for authentication of users
"""
### Libraries
# Third party libraries
from flask import render_template
from flask import request
from flask import flash
from flask import abort
from flask import redirect
from flask import url_for
from flask.views import View
from flask_login import current_user
from flask_login import login_required,login_user, logout_user

# Local imports
from app import db
from . import auth
from ... import views
from .auth_forms import RegistrationForm
from .auth_forms import LoginForm
from ...models import Users


class Register(View):
    """
    Handle requests to register route
    """
    methods = ['GET', 'POST']

    def dispatch_request(self):
        """
        Add an users to database through registraton form
        """
        form = RegistrationForm()
    
        if form.validate_on_submit():
            user = Users(email=form.email.data,
                         username= form.username.data,
                         first_name=form.first_name.data,
                         last_name=form.last_name.data,
                         password=form.password.data)

            db.session.add(user)
            db.session.commit()
            flash('Succesfully registretrd...now u can login:')
            return redirect(url_for('auth.login'))

        
        return render_template('auth/register.html', form=form, title='Register')
auth.add_url_rule('/register', view_func=Register.as_view('register'))



class AdminRegister(View):
    """
    Add an admin to database through registraton form
    """
    methods = ['GET', 'POST']

    def dispatch_request(self):
        """
        Add an admin to database through registraton form
        """
        form = RegistrationForm()
    
        if form.validate_on_submit():
            user = Users(email=form.email.data,
                         username= form.username.data,
                         first_name=form.first_name.data,
                         last_name=form.last_name.data,
                         password=form.password.data,
                         is_admin=True)

            db.session.add(user)
            db.session.commit()
            flash('Succesfully registretrd...now u can login:')
            return redirect(url_for('auth.login'))

        
        return render_template('auth/register.html', form=form, title='Register')
auth.add_url_rule('/adminregister', view_func=AdminRegister.as_view('adminregister'))





'''
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Function for to login user/admin
    """
    form = LoginForm()
    if form.validate_on_submit():

        # Checks any employee exist in database checks the password matches
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            
            login_user(user)

            if user.is_admin:
                
                #return "Adminnnnnn"
                #return redirect(url_for('user.userpage'))
                return redirect(url_for('admin.adminpage'))
            
            else:
                
                #return "Userrrrrrr"
                return redirect(url_for('user.userpage'))

        else:
            
            flash('Invalid email or password')

    return render_template('auth/login.html', form=form, title='Login')
'''


class Login(View):
    """
    """
    methods = ['GET', 'POST']
    
    def dispatch_request(self):
        """
        """
        form = LoginForm()
        if form.validate_on_submit():

            # Checks any employee exist in database checks the password matches
            user = Users.query.filter_by(email=form.email.data).first()
            if user is not None and user.verify_password(form.password.data):
            
                login_user(user)

                if user.is_admin:
                
                    #return "Adminnnnnn"
                    #return redirect(url_for('user.userpage'))
                    return redirect(url_for('admin.adminpage'))
            
                else:
                
                    #return "Userrrrrrr"
                    return redirect(url_for('user.userpage'))

            else:
            
                flash('Invalid email or password')

        return render_template('auth/login.html', form=form, title='Login')
auth.add_url_rule('/login', view_func=Login.as_view('login'))


        

'''
@auth.route('/logout')
@login_required
def logout():
    """
    Function to logout user
    """
    
    logout_user()
    flash('You have  been successfully  logged out.')
    
    return redirect(url_for('auth.login'))
'''

class Logout(View):
    """
    """
    def dispatch_request(self):
        """
        """
        logout_user()
        flash('You have  been successfully  logged out.')
    
        return redirect(url_for('auth.login'))

auth.add_url_rule('/logout', view_func=Logout.as_view('logout'))
