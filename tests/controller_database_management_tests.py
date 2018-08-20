import os
import sys
import unittest
import unittest.mock
import requests_mock
from fixtures.gitlab_mock_api import mock_json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
# add path level above for importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import multi_git_deploy

multi_git_deploy.app.config['TESTING'] = True
multi_git_deploy.app.config['GITLAB_TOKEN_HEADER'] = 'test'
multi_git_deploy.app.config['GITLAB_URL'] = 'mock://gitlab'
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
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'  # in-memory db
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @requests_mock.Mocker()
    def test_track_repo(self, mocker):
        """
        Test adding a repo from the Gitlab API to the db.
        """
        mocker.register_uri(
            'GET',
            'mock://gitlab/projects/4',
            json=mock_json['projects'][0],
            status_code=200
        )
        track_repo(4)
        assert show_repo(4)
        response = self.client.get('/')

    @requests_mock.Mocker()
    def test_add_branch(self, mocker):
        """
        Test adding branches from the Gitlab API to the db.
        """
        mocker.register_uri(
            'GET',
            'mock://gitlab/projects/4',
            json=mock_json['projects'][0],
            status_code=200
        )
        add_branches(4)
        response = self.client.get('/')


if __name__ == '__main__':
    unittest.main()
