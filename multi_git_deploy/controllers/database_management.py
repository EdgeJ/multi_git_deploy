"""
Functions for managing repository database objects
"""
from multi_git_deploy import app
from multi_git_deploy.models.gitlab_repos import (
    db,
    GitRepo,
    GitBranch,
    GitCommit
)


def track_repo(repo_id, repo_name):
    tracked_repo = GitRepo(repo_id, repo_name)
    db.session.add(tracked_repo)
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def show_repo(repo_id):
    return GitRepo.query.get_or_404(repo_id)
