# -*- coding: utf-8 -*-
"""
    multi_git_deploy
    ~~~~~~~~~~~~~~

    Manage and deploy multiple git repositories simultaneously.

    This is the main module that initializes the base app and sets up
    configuration.

    :copyright: (c) 2017 by John Edge.
    :license: MIT, see LICENSE for more details.
"""

from flask import Flask


app = Flask(__name__)
app.config.from_object('multi_git_deploy.settings')
app.config.from_envvar('MULTI_GIT_CONFIG')
