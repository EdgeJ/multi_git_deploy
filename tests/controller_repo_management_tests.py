"""
Unit tests for controllers.repo_management
"""
import os
import sys
import unittest
import unittest.mock

import requests
import requests_mock
from flask import Flask

# add path level above for importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import multi_git_deploy
from tests import TestRunner
from tests.fixtures.gitlab_mock_api import mock_json

# set configurations before importing the controller module
multi_git_deploy.app.config['TESTING'] = True
multi_git_deploy.app.config['GITLAB_TOKEN_HEADER'] = 'test'
multi_git_deploy.app.config['GITLAB_URL'] = 'mock://gitlab'

from multi_git_deploy.controllers import repo_management


@requests_mock.Mocker()
class TestRepo(unittest.TestCase):
    """
    Test controllers responsible for repo management via the Gitlab api.

    Uses static methods for helpers to mock up the api url and call the
    functions from the module for running test cases against
    """
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
            with self.subTest(key=key, val=val):
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

    @staticmethod
    def _merge_accept(mocker):
        mocker.register_uri(
            'PUT',
            'mock://gitlab/projects/1/merge_requests/1/merge',
            json=mock_json['merge_accept'],
        )
        return repo_management.accept_merge(1, 1)

    def test_merge_accept_returns_request_obj(self, mocker):
        self.assertIsInstance(self._merge_accept(mocker), requests.models.Response)

    def test_merge_accept_json_has_keys(self, mocker):
        merge_accept = self._merge_accept(mocker).json()
        for key, val in {
                'id': 1,
                'iid': 1,
                'target_branch': 'master',
                'source_branch': 'test1',
                'title': 'test1',
                'state': 'merged'
        }.items():
            self.assertEqual(merge_accept[key], val)

    def test_merge_accept_status_code_is_200(self, mocker):
        merge_accept = self._merge_accept(mocker)
        self.assertEqual(merge_accept.status_code, 200)

    def test_merge_accept_returns_error_statuses(self, mocker):
        for status in [401, 405, 406, 409]:
            mocker.register_uri(
                'PUT',
                'mock://gitlab/projects/1/merge_requests/1/merge',
                status_code=status
            )
            accept_merge_status_code = repo_management.accept_merge(1, 1).status_code
            self.assertEqual(accept_merge_status_code, status)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner)
