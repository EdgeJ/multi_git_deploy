"""
Default routes for multi_git_deploy
"""
from flask import flash, redirect, render_template, request, url_for
from multi_git_deploy import app
from multi_git_deploy.controllers import database_management, repo_management


@app.route("/")
def index():
    return """
<head>
<title>Multi-deploy</title>
</head>
<body>
<h1>Deploy yer multi-repository project</h1>
<div>
<p>
<a href={0}> View available repos </a>
</p
<p>
<a href={1}>Repo 1</a>
<a href={2}>Repo 2</a>
</p
</div>
    """.format(
        url_for("show_repos"),
        url_for("view_repo", repo=1),
        url_for("view_repo", repo=2)
    )


@app.route("/show_repos")
def show_repos():
    project_list = []
    repos = repo_management.get_repos()
    for project in repos:
        project_list.append(project['name_with_namespace'])
    return "Repos:\n{}".format(project_list)


@app.route("/repo/<int:repo>", methods=['GET', 'DELETE'])
def view_repo(repo):
    if request.method == 'GET':
        return "Repo: {}".format(database_management.show_repo(repo).project_id)
    else:
        flash("This will delete the repo from the database (but not from Gitlab)")
        return "Repo deleted"
