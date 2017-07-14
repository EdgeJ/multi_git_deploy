"""
Controller functions for Gitlab repo management
"""
import requests
from multi_git_deploy import app


class Gitlab:
    """
    Class to define gitlab API methods
    """
    def get_repos(self):
        repos = requests.get(
            '{}/projects'.format(app.config['GITLAB_URL']),
            headers=app.config['GITLAB_TOKEN_HEADER']
        )
        return repos.json()

    def get_branches(self, repo_id):
        branches = requests.get(
            '{url}/projects/{id}/repository/branches'.format(
                url=app.config['GITLAB_URL'],
                id=repo_id
            ),
            headers=app.config['GITLAB_TOKEN_HEADER']
        )
        return branches.json()

    def get_commits(self, repo_id):
        commits = requests.get(
            '{url}/projects/{id}/repository/commits'.format(
                url=app.config['GITLAB_URL'],
                id=repo_id
            ),
            headers=app.config['GITLAB_TOKEN_HEADER']
        )
        return commits.json()
