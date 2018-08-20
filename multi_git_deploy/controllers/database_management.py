# -*- coding: utf-8 -*-
"""
    multi_git_deploy.controllers.database_management
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Functions for managing repository database objects

    :copyright: (c) 2017 by John Edge.
    :license: MIT, see LICENSE for more details.
"""
from sqlalchemy.exc import SQLAlchemyError

from multi_git_deploy.models.gitlab_repos import (
    db,
    GitRepo,
    GitBranch,
    GitCommit
)


def track_repo(repo_json):
    """
    Check if repo is in GitLab and add it to the database.

    :repo_json (dict) JSON data structure representing a Gitlab project.
    :returns (bool) True on success, False otherwise.
    """
    # check for error message in API response, ensure target repo exists
    if 'message' not in repo_json:
        tracked_repo = GitRepo(repo_json['id'], repo_json['name'])
        db.session.add(tracked_repo)
        try:
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
    return False


def add_branches(repo_id, branches):
    """
    Add branches to a repo database object.

    :repo_id (int) ID of the repo to be updated.
    :branches (list) JSON object representing branches for the git repo.
    :return (Bool) True if database is updated, False otherwise.
    """
    repo = GitRepo.query.filter_by(project_id=repo_id).first()
    if repo is not None:
        for branch in branches:
            db.session.add(GitBranch(branch['name'], repo=repo))
        db.session.add(repo)
        try:
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
    return False


# TODO: assess how necessary it is to track commits in the database
#def add_commits(repo_id, branch):
#    """Add commits to a branch of a repository
#
#    :repo_id: TODO
#    :branch: TODO
#    :returns: TODO
#
#    """
#    parent_repo = GitRepo.query.filter_by(project_id=repo_id).first()
#    target_branch = GitBranch.query.filter_by(
#        repo=parent_repo,
#        branch_name=branch
#    ).first()
#    branch_commits = [
#        GitCommit(commit['id'], target_branch)
#        for commit in get_commits(repo_id, branch)
#    ]
#    try:
#        db.session.add(branch_commits)
#        db.session.commit()
#        return True
#    except:
#        db.session.rollback()
#        return False


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
