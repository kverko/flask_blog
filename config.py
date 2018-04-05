class Configuration(object):
    SQLALCHEMY_DATABASE_URI = \
        'postgresql://postgres:postgres@localhost:5432/blog_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECRET_KEY = 'nitk nei wizdiau!'
