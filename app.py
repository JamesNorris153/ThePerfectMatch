from flask import Flask, render_template, request, redirect
from flask_cors import CORS
#Example for importing methods
from users import get_users, create_user, get_user, authenticate_user
from admins import authenticate_admin
from applicant import applicant

app = Flask(__name__, static_url_path='/static')

CORS(app)

## Sends static files when necessary
@app.route('/static/<path:path>')
def send_js(path):
	return send_from_directory('static',path)

## Landing page
@app.route('/')
def index():
	return render_template("index.html")

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

## CV Page - Let user edit/view their cv
@app.route('/applicant/cv')
def show_applicant_cv_page():
	return render_template("applicant_cv.html")
	# NEEDS TO RETURN TEMPLATE WITH CV + USER ID

## Applicant Portal
@app.route('/applicant/login', methods=["GET", "POST"])
def show_applicant_login_page():
	if request.method == "GET":
		return render_template("applicant_portal.html")

	if request.method == "POST":
		email = request.form.get('email')
		password = request.form.get('password')
		# if authenticate_user(email, password):
		# 	return redirect("/applicant/jobs")
		# else:
		# 	return render_template("applicant_portal.html", error="Incorrect username or password")
		if authenticate_user(email, password):
			return "Success"
		else:
			return "Incorrect username or password"

@app.route('/applicant/register', methods=["POST"])
def register_applicant():
	# TODO: check whether a user is already registered under this email
	email = request.form.get('email')
	password = request.form.get('password')
	# confirm_password = request.form.get('confirm_password')

	# if password != confirm_password:
		# return render_template("applicant_portal.html", error="Password's entered do not match")

	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')
	new = applicant(first_name, last_name, email, password)
	create_user(new) #Method could return information e.g. successful registration, email taken, etc.
	# return redirect("/applicant/jobs")
	return "Success"

# Staff Portal
@app.route('/staff/login', methods=["GET", "POST"])
def show_staff_login_page():
	if request.method == "GET":
		return render_template("staff_portal.html")

	if request.method == "POST":
		email = request.form.get('email')
		password = request.form.get('password')
		# if authenticate_admin(email, password):
		# 	return redirect("/staff/jobs")
		# else:
		# 	return render_template("staff_portal.html", error="Incorrect username or password")
		if authenticate_admin(email, password):
			return "Success"
		else:
			return "Incorrect username or password"

## Staff jobs page
@app.route('/staff/jobs')
def show_staff_jobs_page():
    return render_template("staff_jobs.html")

@app.route('/staff/candidates')
def show_staff_candidates_page():
    return render_template("staff_candidates.html")


if __name__ == '__main__':
    app.run(debug=True)
