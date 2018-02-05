# To run

1. Do `pipenv shell` then `gunicorn -k flask_sockets.worker main:app`.
2. Visit http://127.0.0.1:8000.