# cs261

Requirements: Python 2.7

Modules Required:
- flask
- flask_cors
- flask_sqlalchemy
- bcrypt
- sqlite3
- json
- celery

To start app run:
celery worker -A app.celery &
python app.py
