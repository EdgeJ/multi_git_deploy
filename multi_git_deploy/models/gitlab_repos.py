"""
Models for Gitlab Repo database objects
"""
from multi_git_deploy import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


class GitRepo(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), unique=True)
    branches = db.relationship('GitBranch', backref='repo')

    def __init__(self, project_id, project_name):
        self.project_id = project_id
        self.project_name = project_name

    def __repr__(self):
        return '<Repo {}>'.format(repr(self.project_name))


class GitBranch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(100))
    repo_id = db.Column(db.Integer, db.ForeignKey('repo.project_id'))
    commits = db.relationship('GitCommit', backref='branch', nullable=False)

    def __init__(self, branch_name):
        self.branch_name = branch_name

    def __repr__(self):
        return '<Branch {}>'.format(repr(self.branch_name))


class GitCommit(db.Model):
    commit_hash = db.Column(db.String(40), primary_key=True, unique=True)
    commit_author = db.Column(db.String(80))
    commit_date = db.Column(db.String(80))
    commit_message = db.Column(db.String())
    branch = db.Column(db.String(100), db.ForeignKey('branch.id'))

    def __init__(self, commit_hash):
        self.commit_hash = commit_hash

    def __repr__(self):
        return '<Commit {}>'.format(repr(self.commit_hash))
