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
from tests import TestRunner

multi_git_deploy.app.config['TESTING'] = True
multi_git_deploy.app.config['GITLAB_TOKEN_HEADER'] = 'test'
multi_git_deploy.app.config['GITLAB_URL'] = 'mock://gitlab'

from multi_git_deploy.controllers import repo_management


@requests_mock.Mocker()
class TestRepo(TestCase):
    """
    Test controllers responsible for repo management via the Gitlab api.

    Uses static methods for helpers to mock up the api url and call the
    functions from the module for running test cases against
    """
    def create_app(self):
        app = Flask(__name__)
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'  # in-memory db
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def _list_repos(mocker):
        mocker.register_uri(
            'GET',
            'mock://gitlab/projects',
            json=mock_json['projects']
        )
        return repo_management.list_repos()

    def test_list_repos_returns_list(self, mocker):
        self.assertIsInstance(self._list_repos(mocker), list)

    def test_list_repos_first_elem_id_is_four(self, mocker):
        self.assertEqual(4, self._list_repos(mocker)[0]['id'])

    def test_list_repos_second_elem_id_is_six(self, mocker):
        self.assertEqual(6, self._list_repos(mocker)[1]['id'])

    @staticmethod
    def _get_repo(mocker):
        mocker.register_uri(
            'GET',
            'mock://gitlab/projects/4',
            json=mock_json['projects'][0]
        )
        return repo_management.get_repo(4)

    def test_get_repo_returns_json(self, mocker):
        self.assertIsInstance(self._get_repo(mocker), dict)

    def test_get_repo_returns_project_keys(self, mocker):
        for key, val in {
            "id": 4,
            "description": "null",
            "default_branch": "master",
            "name": "Diaspora Client"
        }.items():
            self.assertEqual(self._get_repo(mocker)[key], val)

    @staticmethod
    def _get_branches(mocker):
        mocker.register_uri(
            'GET',
            'mock://gitlab/projects/4/repository/branches',
            json=mock_json['branches']
        )
        return repo_management.get_branches(4)

    def test_get_branches_returns_list(self, mocker):
        self.assertIsInstance(self._get_branches(mocker), list)

    def test_get_branches_has_branch_names(self, mocker):
        self.assertEqual(self._get_branches(mocker)[0]['name'], 'master')
        self.assertEqual(self._get_branches(mocker)[1]['name'], 'development')

    @staticmethod
    def _list_merge_request(mocker, source_branch):
        if source_branch is None:
            uri_str = 'mock://gitlab/projects/4/merge_requests?state=opened'
        else:
            uri_str = 'mock://gitlab/projects/4/merge_requests?state=opened&source_branch={source}'.format(
                source=source_branch
            )

        mocker.register_uri(
            'GET',
            uri_str,
            json=mock_json['merge_request']
        )
        return repo_management.list_merge_requests(4, source_branch)

    def test_list_merge_requests_with_source_branch_none_returns_list(self, mocker):
        self.assertIsInstance(self._list_merge_request(mocker, None), list)

    def test_list_merge_requests_with_source_branch_master_returns_list(self, mocker):
        self.assertIsInstance(self._list_merge_request(mocker, 'master'), list)




if __name__ == '__main__':
    unittest.main(testRunner=TestRunner)
