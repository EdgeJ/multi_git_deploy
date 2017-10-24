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

API_SESSION = requests.Session()
API_SESSION.headers.update(app.config['GITLAB_TOKEN_HEADER'])


def list_repos():
    """
    Return json object of all repos.
    """
    repos = API_SESSION.get(
        '{}/projects'.format(app.config['GITLAB_URL']),
    )
    return repos.json()


def get_repo(repo_id):
    """
    Return json object of a single repo.
    """
    repo = API_SESSION.get(
        '{url}/projects/{repo_id}'.format(
            url=app.config['GITLAB_URL'],
            repo_id=repo_id
        )
    )
    return repo.json()


def get_branches(repo_id):
    """
    Return json object of all branches of a repo.
    """
    branches = API_SESSION.get(
        '{url}/projects/{id}/repository/branches'.format(
            url=app.config['GITLAB_URL'],
            id=repo_id
        )
    )
    return branches.json()


def get_commits(repo_id, branch):
    """
    Return json object of all commits for a branch of a repo.
    """
    commits = API_SESSION.get(
        '{url}/projects/{id}/repository/commits?ref_id={branch}'.format(
            url=app.config['GITLAB_URL'],
            id=repo_id,
            branch=branch
        )
    )
    return commits.json()


def show_diff(repo_id, commit_hash):
    """TODO: Docstring for show_diff.

    :repo_id: id of the repo.
    :commit_hash: SHA hash of the commit to show a diff for.
    :returns: TODO

    """
    diff = API_SESSION.get(
        '{url}/projects/{id}/repository/commits/{sha}/diff'.format(
            url=app.config['GITLAB_URL'],
            id=repo_id,
            sha=commit_hash
        )
    )
    return diff.json()


def cherry_pick(repo_id, target_branch, commit_hash):
    """
    Cherry pick a commit into another branch via the Gitlab API.

    :repo_id: id of the repo to commit to.
    :target_branch: target branch to commit to.
    :commit_hash: SHA hash for the commit being cherry picked.
    :returns: JSON object from the Gitlab API request.

    """
    commit_string = API_SESSION.post(
        '{url}/projects/{id}/repository/commits/{hash}/cherry_pick'.format(
            url=app.config['GITLAB_URL'],
            id=repo_id,
            hash=commit_hash
        ), data={'branch': target_branch}
    )
    return commit_string.json()
