from flask import Flask, render_template, request
from flask_cors import CORS
#Example for importing methods
from models.users import get_users, create_user, get_user

app = Flask(__name__, static_url_path='/static')

CORS(app)

## Sends static files when necessary
@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static',path)

## Landing page
@app.route('/')
def index():
    return render_template('index.html')

## Internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")

## Page not found
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

## Jobs page - default page for users not logged in
@app.route('/jobs')
def show_jobs_page():
    return render_template("jobs.html")

if __name__ == '__main__':
    app.run(debug=True)
