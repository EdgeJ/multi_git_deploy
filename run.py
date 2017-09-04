#!/usr/bin/env python
from multi_git_deploy.routes import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
