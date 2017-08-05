import sys
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
# Add top level directory to the path to allow us to import a module from a
# directory tree above the cwd
sys.path.insert(0, '../')
from multi_git_deploy.models.gitlab_repos import db
from multi_git_deploy.controllers.database_management import (
    track_repo,
    add_branches,
    show_repo
)


class TestRepoTrack(TestCase):
    """
    Test tracking repos in the database.
    """
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'  # in-memory db
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_track_repo(self):
        """
        Test adding a repo from the Gitlab API to the db.
        """
        track_repo(1)
        assert show_repo(1)
        response = self.client.get('/')

    def test_add_branch(self):
        """
        Test adding branches from the Gitlab API to the db.
        """
        add_branches(1)
        response = self.client.get('/')


if __name__ == '__main__':
    unittest.main()
