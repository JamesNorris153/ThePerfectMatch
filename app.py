from flask import Flask, render_template, request, redirect, Response
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
	if request.cookies.get("logged_on") == "applicant":
		return redirect("/applicant/jobs")
	if request.cookies.get("logged_on") == "admin":
		return redirect("/staff/candidates")
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
@app.route("/applicant/jobs")
def show_applicant_jobs_page():
	return render_template("applicant_jobs.html")

## CV Page - Let user edit/view their cv
@app.route('/applicant/cv', methods=["GET"])
def show_applicant_cv_page():
	return render_template("applicant_cv.html")
	# NEEDS TO RETURN TEMPLATE WITH CV + USER ID

@app.route('/applicant/save_cv', methods=["POST"])
def save_applicant_cv():
    cv = request.form.get('cv')
    # DO SOMETHING WITH JSON CV
    return Response("Success", status=200, mimetype="text/html")

## Applicant Portal
@app.route('/applicant/login', methods=["GET", "POST"])
def show_applicant_login_page():
	if request.method == "GET":
		return render_template("applicant_portal.html")

	if request.method == "POST":
		email = request.form.get('email')
		password = request.form.get('password')
		if authenticate_user(email, password):
			response = Response("Success", status=200, mimetype="text/html")
			response.set_cookie("logged_on", value="applicant")
			return response
		else:
			return Response("Incorrect username or password", status=200, mimetype="text/html")

@app.route('/applicant/register', methods=["POST"])
def register_applicant():
	# TODO: check whether a user is already registered under this email
	email = request.form.get('email')
	password = request.form.get('password')
	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')
	new = applicant(first_name, last_name, email, password)
	user_id = create_user(new)

	response = Response("Success", status=200, mimetype="text/html")
	response.set_cookie("logged_on", value="applicant")
	return response

# Staff Portal
@app.route('/staff/login', methods=["GET", "POST"])
def show_staff_login_page():
	if request.method == "GET":
		return render_template("staff_portal.html")

	if request.method == "POST":
		email = request.form.get('email')
		password = request.form.get('password')
		if authenticate_admin(email, password):
			response = Response("Success", status=200, mimetype="text/html")
			response.set_cookie("logged_on", value="admin")
			return response
		else:
			return Response("Incorrect username or password", status=200, mimetype="text/html")

## Staff jobs page
@app.route('/staff/jobs')
def show_staff_jobs_page():
    return render_template("staff_jobs.html")

@app.route('/staff/candidates')
def show_staff_candidates_page():
    return render_template("staff_candidates.html")


if __name__ == '__main__':
    app.run(debug=True)
