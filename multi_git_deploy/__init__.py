from flask import Flask


app = Flask(__name__)
app.config.from_object('multi_git_deploy.settings')
app.config.from_envvar('MULTI_GIT_CONFIG')
