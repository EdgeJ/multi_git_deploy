"""
File: database_management.py
Author: John Edge
Email: edge.jm@gmail.com
Github: https://github.com/edgej
Description: Functions for managing repository database objects
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


def show_repo(repo_id):
    return GitRepo.query.get_or_404(repo_id)
