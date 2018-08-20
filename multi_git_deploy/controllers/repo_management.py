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
API_SESSION.headers.update(
    {'private-token': app.config['GITLAB_TOKEN_HEADER']}
)

GITLAB_URL = app.config['GITLAB_URL']


def list_repos():
    """
    Return json object of all repos.
    """
    repos = API_SESSION.get(
        '{}/projects'.format(GITLAB_URL),
    )
    return repos.json()


def get_repo(repo_id):
    """
    Return json object of a single repo.
    """
    repo = API_SESSION.get(
        '{url}/projects/{repo_id}'.format(
            url=GITLAB_URL,
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
            url=GITLAB_URL,
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
            url=GITLAB_URL,
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
            url=GITLAB_URL,
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
            url=GITLAB_URL,
            id=repo_id,
            hash=commit_hash
        ), data={'branch': target_branch}
    )
    return commit_string.json()


def list_merge_requests(repo_id, source_branch=None):
    """TODO: Docstring for list_merge_requests.
    :returns: TODO

    """
    if source_branch is not None:
        request_string = '{url}/projects/{id}/merge_requests?state=opened&source_branch={source}'.format(
            url=GITLAB_URL,
            id=repo_id,
            source=source_branch
        )
    else:
        request_string = '{url}/projects/{id}/merge_requests?state=opened'.format(
            url=GITLAB_URL,
            id=repo_id
        )

    merge_requests = API_SESSION.get(request_string)
    return merge_requests.json()


def show_merge_changes(repo_id, mr_id):
    """TODO: Docstring for show_merge_changes.

    :repo_id: TODO
    :returns: TODO

    """
    changes = API_SESSION.get(
        '{url}/projects/{id}/merge_requests/{merge_id}/changes'.format(
            url=GITLAB_URL,
            id=repo_id,
            merge_id=mr_id
        )
    )
    return changes.json()


def accept_merge(repo_id, mr_id):
    """TODO: Docstring for accept_merge.
    :returns: TODO

    """
    merge_accept = API_SESSION.put(
        '{url}/projects/{id}/merge_requests/{merge_id}/merge'.format(
            url=GITLAB_URL, id=repo_id, merge_id=mr_id
        )
    )
    return merge_accept
