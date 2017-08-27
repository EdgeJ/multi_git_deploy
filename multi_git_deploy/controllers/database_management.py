# -*- coding: utf-8 -*-
"""
    multi_git_deploy.controllers.database_management
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Functions for managing repository database objects

    :copyright: (c) 2017 by John Edge.
    :license: MIT, see LICENSE for more details.
"""

from multi_git_deploy import app
from multi_git_deploy.controllers.repo_management import (
    get_branches,
    get_commits,
    get_repo
)
from multi_git_deploy.models.gitlab_repos import (
    db,
    GitRepo,
    GitBranch,
    GitCommit
)


def track_repo(repo_id):
    """
    Check if repo is in GitLab and add it to the database.
    """
    api_response = get_repo(repo_id)
    # check for error message in API response, ensure target repo exists
    if 'message' not in api_response:
        tracked_repo = GitRepo(api_response['id'], api_response['name'])
        db.session.add(tracked_repo)
        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False


def add_branches(repo_id):
    """
    Add branches to a repo database object.

    Returns:
        True if database is updated
        False if the database transaction fails
        None if the repo database object is not found
    """
    repo = GitRepo.query.filter_by(project_id=repo_id).first()
    if repo is not None:
        api_branches = get_branches(repo_id)
        # list comprehension to generate multiple GitBranch instances
        db_branches = [
            GitBranch(api_branch['name'], repo=repo)
            for api_branch in api_branches
        ]
        db.session.add(repo)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return False
        return True


def add_commits(repo_id, branch):
    """Add commits to a branch of a repository

    :repo_id: TODO
    :branch: TODO
    :returns: TODO

    """
    parent_repo = GitRepo.query.filter_by(project_id=repo_id).first()
    target_branch = GitBranch.query.filter_by(
        repo=parent_repo,
        branch_name=branch
    ).first()
    branch_commits = [
        GitCommit(commit['id'], target_branch)
        for commit in get_commits(repo_id, branch)
    ]
    try:
        db.session.add(branch_commits)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def show_repo(repo_id):
    return GitRepo.query.get_or_404(repo_id)


def repo_in_database(repo_id):
    """
    A boolean to search for a repo id in the database

    Args:
        repo_id (int): id to search the database for.
    Returns:
        True if the repo id is found in the database, False if not.
    """
    if GitRepo.query.get(repo_id) is not None:
        return True
    return False
