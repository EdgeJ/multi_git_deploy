"""
Controller functions for Gitlab repo management
"""
import requests
from multi_git_deploy import app
from multi_git_deploy.models.gitlab_repos import (
    db,
    GitRepo,
    GitBranch,
    GitCommit
)


#############################################
## Functions for managing Gitlab API requests
#############################################
def get_repos():
    """
    Return json object of all repos.
    """
    repos = requests.get(
        '{}/projects'.format(app.config['GITLAB_URL']),
        headers=app.config['GITLAB_TOKEN_HEADER']
    )
    return repos.json()


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


####################################################
# Functions for managing repository database objects
####################################################
def track_repo(repo_id, repo_name):
    tracked_repo = GitRepo(repo_id, repo_name)
    db.session.add(tracked_repo)
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False
