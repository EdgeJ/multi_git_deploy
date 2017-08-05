# -*- coding: utf-8 -*-
"""
    multi_git_deploy.controllers.repo_management
    ~~~~~~~~~~~~~~~~~~~~~

    Controller functions for Gitlab API calls.

    :copyright: (c) 2017 by John Edge.
    :license: MIT, see LICENSE for more details.
"""

import requests
from multi_git_deploy import app


def list_repos():
    """
    Return json object of all repos.
    """
    repos = requests.get(
        '{}/projects'.format(app.config['GITLAB_URL']),
        headers=app.config['GITLAB_TOKEN_HEADER']
    )
    return repos.json()


def get_repo(repo_id):
    """
    Return json object of a single repo.
    """
    repo = requests.get(
        '{url}/projects/{repo_id}'.format(
            url=app.config['GITLAB_URL'],
            repo_id=repo_id
        ),
        headers=app.config['GITLAB_TOKEN_HEADER']
    )
    return repo.json()


def get_branches(repo_id):
    """
    Return json object of all branches of a repo.
    """
    branches = requests.get(
        '{url}/projects/{id}/repository/branches'.format(
            url=app.config['GITLAB_URL'],
            id=repo_id
        ),
        headers=app.config['GITLAB_TOKEN_HEADER']
    )
    return branches.json()


def get_commits(repo_id):
    """
    Return json object of all commits in a repo.
    """
    commits = requests.get(
        '{url}/projects/{id}/repository/commits'.format(
            url=app.config['GITLAB_URL'],
            id=repo_id
        ),
        headers=app.config['GITLAB_TOKEN_HEADER']
    )
    return commits.json()
