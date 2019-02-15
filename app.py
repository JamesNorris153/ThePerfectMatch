from flask import Flask, render_template, request, redirect
from flask_cors import CORS
<<<<<<< HEAD

=======
from models import authenticate
>>>>>>> james
#Example for importing methods
from users import get_users, create_user, get_user

app = Flask(__name__, static_url_path='/static')

CORS(app)

## Sends static files when necessary
@app.route('/static/<path:path>')
def send_js(path):
	return send_from_directory('static',path)

## Landing page
@app.route('/', methods=['GET', 'POST'])
def index():
    # Might be worth checking if user is already logged in -> Take to correct access page
    return redirect("/applicant/jobs")

	if request.method == "GET":
		return render_template('index.html')

	if request.method == "GET":
		username = request.form.get('username')
		password = request.form.get('password')
		if authenticate(username, password):
			return 'Template not yet implemented'
		else:
			return render_template('index.html', error = "Incorrect username or password")

## Internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")

## Page not found
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

## Jobs page - default page for users not logged in
@app.route('/applicant/jobs')
def show_applicant_jobs_page():
    return render_template("applicant_jobs.html")

## Applicant Portal
@app.route('/applicant/login')
def show_applicant_login_page():
    return render_template("applicant_portal.html")

# Staff Portal
@app.route('/staff/login')
def show_staff_login_page():
    return render_template("staff_portal.html")

## Staff jobs page
@app.route('/staff/jobs')
def show_staff_jobs_page():
    return render_template("staff_jobs.html")

@app.route('/staff/candidates')
def show_staff_candidates_page():
    return render_template("staff_candidates.html")


if __name__ == '__main__':
    app.run(debug=True)
