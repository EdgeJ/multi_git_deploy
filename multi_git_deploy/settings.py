import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
    os.path.join(basedir, 'multi_deploy.db')
)
DATABASE_CONNECT_OPTIONS = {}

del os
