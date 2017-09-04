# -*- coding: utf-8 -*-
"""
    multi_git_deploy.routes
    ~~~~~~~~~~~~~

    Default routes for multi_git_deploy

    :copyright: (c) 2017 by John Edge.
    :license: MIT, see LICENSE for more details.
"""

import requests
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
</div>
    """.format(
        url_for('show_repos'),
    )


@app.route("/show_repos")
def show_repos():
    """
    Show a list of all repositories available on the Gitlab server.

    Returns:
        A rendered template with all repos or a 503 error if the service cannot
        connect to the remote Gitlab service.
    """
    project_list = []
    try:
        repos = repo_management.list_repos()
    except requests.exceptions.ConnectionError:
        return "Error connecting to Gitlab", 503
    for project in repos:
        project_list.append(project)
    return render_template('show_repos.html', project_list=project_list)


@app.route("/repo/<int:repo>", methods=['GET', 'POST', 'DELETE'])
def view_repo(repo):
    """
    When called with an HTTP GET method, views the details of a repository
    tracked in the database. When called with POST or DELETE, either tracks
    or deletes the repository in the database.

    Arguments:
        repo (int): The repo id of the repository object.
    Returns:
        A redirect function.
    """
    if request.method == 'GET':
        return "Repo: {}".format(
            database_management.show_repo(repo).project_id
        )
    elif request.method == 'POST':
        if database_management.repo_in_database(repo):
            flash("Repository is already tracked in the database")
        else:
            database_management.track_repo(repo)
            flash("Repository added to the database.")
        return redirect("/repo/{}".format(repo))
    elif request.method == 'DELETE':
        flash("Repo deleted")
        return redirect("/")
