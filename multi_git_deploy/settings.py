# -*- coding: utf-8 -*-
"""
    multi_git_deploy.settings
    ~~~~~~~~~~~~~~

    Default settings for the multi_git_deploy application.

    These may be overridden by other configs specified in a file bound to the
    MULTI_GIT_CONFIG environment variable.

    :copyright: (c) 2017 by John Edge.
    :license: MIT, see LICENSE for more details.
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
    os.path.join(basedir, 'multi_deploy.db')
)
DATABASE_CONNECT_OPTIONS = {}

del os
