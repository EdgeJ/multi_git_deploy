# -*- coding: utf-8 -*-
"""
    multi_git_deploy
    ~~~~~~~~~~~~~~

    Manage and deploy multiple git repositories simultaneously.

    This is the main module that initializes the base app and sets up
    configuration.

    :copyright: (c) 2018 by John Edge.
    :license: MIT, see LICENSE for more details.
"""

import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask


app = Flask(__name__)
app.config.from_object('multi_git_deploy.settings')


def log_setup():
    """
    Set up logging

    Create a logfile in the directory specified by our settings and rotate the
    log when it's larger than 500kb
    """

    try:
        logpath = app.config['LOGPATH']
    except KeyError:
        logpath = '.'

    if os.path.exists(logpath):
        log_file = '{path}/multi-git-deploy.log'.format(path=logpath)
    else:
        raise IOError

    rotating_logfile = RotatingFileHandler(
        log_file,
        maxBytes=512000,  # rotate every 500Kb
        backupCount=4  # keep 4 copies of the log
    )

    if app.config['DEBUG']:
        rotating_logfile.setLevel(logging.DEBUG)
    else:
        rotating_logfile.setLevel(logging.ERROR)

    app.logger.addHandler(rotating_logfile)
