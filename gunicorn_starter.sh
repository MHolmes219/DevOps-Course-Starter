#!/bin/sh
poetry run gunicorn --chdir todo_app 'todo_app.app:create_app()' -b 0.0.0.0:${PORT:-5000} --access-logfile /var/log/gunicorn-access.log --error-logfile /var/log/gunicorn-error.log
