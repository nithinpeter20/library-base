#config.py
"""
config.py
~~~~~~~~~~~~~~~

A script to do basic configurations
"""

class Config(object):
    """
    Common configurations
    """


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    #MEDIA_PATH = "D:\User\ nithin_peter\Python flask\New folder\LibraryMgmnt1\media"
    UPLOAD_FOLDER = '/media'
    
class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = True

app_config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig
}
