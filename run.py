"""
run.py
~~~~~~~~~~~~~~~

A script to run flask app
"""
#### Libraries
# Standard library
import os

#local imports
from app import create_app
from app import db

CONFIG_NAME = os.getenv('FLASK_CONFIG')
app = create_app(CONFIG_NAME)

if __name__ == '__main__':
    db.create_all()
    manager.run()
    app.run(debug='True')
    
    