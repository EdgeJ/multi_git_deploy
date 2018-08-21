import sys
import unittest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase

from tests import TestRunner
# Add top level directory to the path to allow us to import a module from a
# directory tree above the cwd
sys.path.insert(0, '../')
from multi_git_deploy.models.gitlab_repos import (
    db,
    GitRepo,
    GitBranch,
    GitCommit
)


class TestRepoCreate(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"  # In-memory db
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_init(self):
        repo = GitRepo(1, 'puppet / nginx')
        db.session.add(repo)
        db.session.commit()
        assert repo in db.session
        response = self.client.get("/")

    def test_add_branch(self):
        repo = GitRepo(1, 'puppet / nginx')
        branch = GitBranch('master', repo=repo)
        db.session.add(repo)
        db.session.commit()
        assert branch in db.session
        response = self.client.get("/")

    def test_add_commit(self):
        repo = GitRepo(1, 'puppet / nginx')
        branch = GitBranch('master', repo=repo)
        commit = GitCommit(
            '945469986d00c9255cbe1fe823ad0f2991b7371e',
            branch=branch
        )
        commit.author = 'John Doe'
        commit.message = 'Adding awesome features'
        db.session.add(repo)
        assert commit in db.session
        response = self.client.get("/")


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner)
