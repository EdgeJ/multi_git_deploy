"""
Models for Gitlab Repo database objects
"""
from multi_git_deploy import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


class GitRepo(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), unique=True)

    def __init__(self, project_id, project_name):
        self.project_id = project_id
        self.project_name = project_name

    def __repr__(self):
        return '<Repo {}>'.format(repr(self.project_name))


class GitBranch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(100))
    repo_id = db.Column(db.Integer,db.ForeignKey('git_repo.project_id'))
    repo = db.relationship('GitRepo', backref=db.backref('branch'))

    def __init__(self, branch_name, repo=None):
        self.branch_name = branch_name
        if isinstance(repo, GitRepo):
            self.repo = repo

    def __repr__(self):
        return '<Branch {}>'.format(repr(self.branch_name))


class GitCommit(db.Model):
    git_hash = db.Column(db.String(40), primary_key=True, unique=True)
    author = db.Column(db.String(80))
    date = db.Column(db.String(80))
    message = db.Column(db.String())
    branch_id = db.Column(db.Integer, db.ForeignKey('git_branch.id'))
    branch = db.relationship('GitBranch', backref='commit')

    def __init__(self, git_hash, branch=None):
        self.git_hash = git_hash
        if isinstance(branch, GitBranch):
            self.branch = branch

    def __repr__(self):
        return '<Commit {}>'.format(repr(self.commit_hash))
