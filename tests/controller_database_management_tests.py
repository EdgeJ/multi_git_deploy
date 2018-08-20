"""
Unit tests for controllers.database_management
"""
import os
import sys
import unittest
import unittest.mock

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase

# add path level above for importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import multi_git_deploy
from fixtures.gitlab_mock_api import mock_json
from tests import TestRunner

# set config before importing modules
multi_git_deploy.app.config['TESTING'] = True

from multi_git_deploy.models.gitlab_repos import db, GitRepo
from multi_git_deploy.controllers import database_management


class TestDatabaseController(TestCase):
    """
    Test controllers responsible for managing the SQL database
    """
    def create_app(self):
        app = Flask(__name__)
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'  # in-memory db
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()
        db.session.add(GitRepo(project_id=1, project_name='foo'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_track_repo(self):
        """
        Test adding a repo from the Gitlab API to the db.
        """
        self.assertTrue(
            database_management.track_repo(mock_json['projects'][0])
        )

    def test_add_branch(self):
        """
        Test adding branches from the Gitlab API to the db.
        """
        self.assertTrue(
            database_management.add_branches(1, mock_json['branches'])
        )

    def test_show_repo(self):
        database_management.show_repo(1)

    def test_repo_in_database(self):
        self.assertTrue(
            database_management.repo_in_database(1)
        )


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner)
