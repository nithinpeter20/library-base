#app/__init__.py
"""
Script for running flask 
"""

# Third-party libraries
from flask import Flask
from flask import current_app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_script import Manager
from flask_migrate import MigrateCommand

# Local imports
from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    """
    This function creates app
    """
    app = Flask(__name__, static_url_path='/static', instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    Bootstrap(app)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    from .views.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .views.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views.user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')
    
    return app