from multi_git_deploy import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


class GitRepo(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), unique=True)
    branches = db.Column(db.String(50))

    def __init__(self, project_id, project_name):
        self.project_id = project_id
        self.project_name = project_name

    def __repr__(self):
        return '<Repo %r>' % self.project_name
