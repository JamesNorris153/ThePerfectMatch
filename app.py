from flask import Flask, render_template, request, redirect, Response, session
from flask_cors import CORS
import json

from users import *
# from ml import retrain
import os

## Session variables
# account_type : "Admin"/"Applicant"/None : Shows type of account logged in user has, or shows user isn't logged in
# user_id : Stores logged in user id from database

## NOTE: WHEN CONNECTING TO THE DATABASE, USE TRY EXCEPT BLOCKS INCASE OF DATABASE DISCONNECT OR ANY OTHER ISSUE

app = Flask(__name__, static_url_path='/static')

CORS(app)

## Function to check whether user is logged in
# Returns account_type or None if not logged in
# If either session variable has been lost, log user out and return None
def login_check():
	user_id = session.get("user_id")
	account_type = session.get("account_type")
	if user_id is None or account_type is None:
		logout()
		return None
	else:
		return account_type

# Function to reset all session variables
def logout():
	session.clear()

## Sends static files when necessary
@app.route("/static/<path:path>")
def send_js(path):
	return send_from_directory("static", path)

## Internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")

## Page not found
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

## Landing page
@app.route("/")
def index():
	account_type = login_check()
	if account_type is None:
		return render_template("index.html")
	elif account_type == "Admin":
		return redirect("/staff/jobs")
	else:
		return redirect("/applicant/jobs")

## Logout user
@app.route("/logout")
def logout_user():
	session.clear()
	return redirect("/")

## Staff Pages ##

## Staff Login Page
# GET: Return staff_portal page
# POST: Try to authenticate staff member
@app.route("/staff/login", methods=["GET", "POST"])
def staff_login():
	# creates a dummy admin with username "test" and password "test" for testing
	# test = admin("test", "test")
	# create_admin(test)

	# Requesting Page
	if request.method == "GET":
		# If staff already logged in, go to homepage
		if login_check() == "Admin":
			return redirect("/staff/jobs")
		return render_template("staff_portal.html")

	# Receives: Email + Password
	# Returns: Success/Failure
	# Actions: Set SESSION account_type + user_id
	if request.method == "POST":
		# GET REQUIRED REQUEST PARAMETERS
		email = request.form.get("email")
		password = request.form.get("password")

		try:
			# Check if valid login -> Method should return user_id OR None
			user_id = authenticate_admin(email, password)
			if user_id is None:
				# if None returned, email or password is incorrect
				return Response("Incorrect username or password", status=200, mimetype="text/html")
			else:
				session["account_type"] = "Admin"
				session["user_id"] = user_id
				return Response("Success", status=200, mimetype="text/html")
		except:
			return Response("There was an issue logging you in, please try again", status=200, mimetype="text/html")

## Staff Jobs Page
@app.route("/staff/jobs")
def show_staff_jobs_page():
	if login_check() == "Admin":
		return render_template("staff_jobs.html")
	return redirect("/")

## Get All Jobs - Staff
# Returns: All jobs created by this user in JSON/Text Format
@app.route("/staff/get_jobs")
def get_staff_jobs():
	if login_check() == "Admin":

		# GET ALL JOBS IN JSON FORMAT
		try:
			jobs = get_jobs()
			jobs_dict = create_jobs_dictionary(jobs)
			jobs_json = json.dumps(jobs_dict)
		except:
			return Response("Could not connect to the database", status=200, mimetype="text/html")

		return Response(jobs_json, status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")

## Staff Candidates Page
@app.route("/staff/candidates")
def show_staff_candidates_page():
	if login_check() == "Admin":
		job_id = request.args.get('job_id')
		if job_id is None:
			session['job_id'] = None
			return redirect("/staff/jobs")
		session['job_id'] = job_id
		return render_template("staff_candidates.html")
	return redirect("/")

## Get All Candidates - Staff
# Returns: All candidates for jobs by this user in JSON/Text format
@app.route("/staff/get_candidates")
def get_candidates():
	if login_check() == "Admin":
		# GET REQUIRED REQUEST PARAMETERS
		job_id = request.args.get("job_id")
		if session['job_id'] is None:
			return Response("Could not find candidates for this job, please reload the page", status=200, mimetype="text/html")
		# GET ALL THIS JOB CREATED BY THIS USER IN JSON FORMAT
		# candidates = [
		# {
		# 	"ID":candidate_id,
		# 	"First Name":first_name,
		# 	"Last Name":last_name,
		# 	"Email":email,
		# 	"Score":score,
		# 	"CVID":cvid,
		# 	"Status":status ("Like"/"Dislike"/"Unknown")
		# }
		# ]
		try:
			candidates = show_best_candidates(job_id)
			candidates_json = json.dumps(candidates)
		except:
			return Response("Could not retrieve data from the database", status=200, mimetype="text/html")

		return Response(candidates_json, status=200, mimetype="json/application")
	return Response("You are not logged in", status=200, mimetype="text/html")

## Get a CV from database to view
# Receives: cv_id
# Returns: CV in JSON/Text Format
@app.route("/staff/get_cv", methods=["POST"])
def get_cv_by_id():
	if login_check() == "Admin":
		# GET REQUIRED REQUEST PARAMETERS
		cv_id = request.form.get('cv_id')

		try:
			cv = get_CV(cv_id)
			cv_json = jsonify_cv(cv)
		except:
			return Response("Could not connect to the database", status=200, mimetype="text/html")

		return Response(cv_json, status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")

## Like a candidate for a role
# Receives: cv_id
# Returns: Success/Failure
# Actions: Likes candidate in DB to adapt ML
@app.route("/staff/like_candidate", methods=["POST"])
def like_candidate():
	if login_check() == "Admin":
		# GET REQUIRED REQUEST PARAMETERS
		cv_id = request.form.get("cv_id")
		job_id = session["job_id"]

		# LIKE CANDIDATE FOR ROLE
		try:
			# cv_id = None
			# applications = show_current_applications(user_id)
			# for application in applications:
			# 	if application[0] == jobID:
			# 		cv_id = application[1]
			update_status(job_id, cv_id, 1)
		except:
			return Response("Could not connect to the database", status=200, mimetype="text/html")

		return Response("Success", status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")

## Dislike a candidate for a role
# Receives: cv_id
# Returns: Success/Failure
# Actions: Dislikes candidate in DB to adapt ML
@app.route("/staff/dislike_candidate", methods=["POST"])
def dislike_candidate():
	if login_check() == "Admin":
		# GET REQUIRED REQUEST PARAMETERS
		cv_id = request.form.get("cv_id")
		job_id = session["job_id"]

		# DISLIKE CANDIDATE FOR ROLE
		try:
			# cv_id = None
			# applications = show_current_applications(candidate_id)
			# for application in applications:
			# 	if application[0] == jobID:
			# 		cv_id = application[1]
			update_status(job_id, cv_id, 2)
		except:
			return Response("Could not connect to the database", status=200, mimetype="text/html")

		return Response("Success", status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")

## Create/Edit A Job
# Receives: job_id + job details in JSON Format (If new job, job_id passed is -1)
#	var job = {
#		"Name":job_name,
#		"Description":job_description,
#		"Deadline":job_deadline,
#		"Location":job_location,
#		"Position":job_position,
#		"Status":job_status,
#		"Questions":[{
#			"Question":question,
#			"Correct":correct_answer,
#			"Incorrect":[{
#				"Answer":answer
#			}],
# 		"QuestionNumber":number of questions to be randomly given to applicant
#		}]
#	};
# Returns: Success/Failure
# Actions: Add Job to database or update it's details
@app.route("/staff/save_job", methods=["POST"])
def save_job():
	if login_check() == "Admin":
		# GET REQUIRED REQUEST PARAMETERS
		user_id = session["user_id"]
		job_id = request.form.get("job_id")
		job_json = json.loads(request.form.get("job"))

		# CREATE JOB IN DATABASE
		job = Job(
			job_json["Name"],
			job_json["Description"],
			job_json["Deadline"],
			job_json["Location"],
			job_json["Position"],
			job_json["Status"])
		try:
			if job_id == -1:
				insert_job(job)
				return Response("Success", status=200, mimetype="text/html")
			else:
				# TODO: edit job method
				close_job(job_id)
				insert_job(job)
				return Response("Success", status=200, mimetype="text/html")
		except:
			return Response("Could not connect to the database", status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")

@app.route("/staff/delete_job", methods=["POST"])
def delete_job():
	if login_check() == "Admin":
		# GET REQUIRED REQUEST PARAMETERS
		job_id = request.form.get("job_id")

		# DELETE JOB IN DATABASE
		try:
			close_job(job_id)
		except:
			return Response("Could not connect to the database", status=200, mimetype="text/html")

		return Response("Success", status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")

@app.route("/staff/retrain_job", methods=["POST"])
def retrain_job():
	if login_check() == "Admin":
		# GET REQUIRED REQUEST PARAMETERS
		job_id = request.form.get("job_id")

		# PERFORM ML RETRAINING
		try:
			print()
			# retrain(job_id)
		except:
			return Response("Could not update data in the database", status=200, mimetype="text/html")

		return Response("Success", status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")

## Applicant Pages

# Applicant Login Page
# GET: Return applicant_portal page
# POST: Try to authenticate applicant
@app.route("/applicant/login", methods=["GET","POST"])
def applicant_login():

	# Requesting Page
	if request.method == "GET":
		# If applicant already logged in, go to homepage
		if login_check() == "Applicant":
			return redirect("/applicant/jobs")
		return render_template("applicant_portal.html")

	# Receives: Email + Password
	# Returns: Success/Failure
	# Actions: Set SESSION account_type + user_id
	if request.method == "POST":
		# GET REQUIRED REQUEST PARAMETERS
		email = request.form.get("email")
		password = request.form.get("password")

		try:
			# Check if valid user logging in -> Method should return user_id OR None
			user_id = authenticate_user(email, password)
			if user_id is None:
				# if None returned, email or password is incorrect
				return Response("Incorrect username or password", status=200, mimetype="text/html")
			else:
				session["account_type"] = "Applicant"
				session["user_id"] = user_id
				return Response("Success", status=200, mimetype="text/html")
		except:
			return Response("There was an issue logging you in, please try again", status=200, mimetype="text/html")

# Applicant Registration POST Method
# Receives: email, password, first name, last name
# Returns: Success/Failure
# Actions: Create new applicant in database + Set SESSION variables
@app.route("/applicant/register", methods=["POST"])
def register_applicant():

	# GET REQUIRED REQUEST PARAMETERS
	FName = request.form.get("first_name")
	LName = request.form.get("last_name")
	email = request.form.get("email")
	password = request.form.get("password")

	try:
		# If the email address is taken, return an error
		if not check_mail(email):
			return Response("This email address is taken", status=200, mimetype="text/html")

		new_applicant = Applicant(FName, LName, password, email)
		user_id = create_user(new_applicant)
		session["account_type"] = "Applicant"
		session["user_id"] = user_id
		return Response("Success", status=200, mimetype="text/html")
	except:
		return Response("There was an error creating your account, please try again", status=200, mimetype="text/html")

## Applicant Jobs Page
@app.route("/applicant/jobs")
def show_applicant_jobs_page():
	if login_check() == "Applicant":
		return render_template("applicant_jobs.html")
	return redirect("/")

## Get All Jobs - Applicant
@app.route("/applicant/get_jobs")
def get_applicant_jobs():
	if login_check() == "Applicant":
		# GET REQUIRED SESSION PARAMETER
		user_id = session["user_id"]

		# GET ALL JOBS IN JSON FORMAT - Signify whether user has Not Applied / Applied But Not Taken Test / Received Feedback
		try:
			jobs = get_jobs()
			jobs_dict = create_jobs_dictionary(jobs)
			current_applications = show_current_applications(user_id)
			for job in jobs_dict:
				if job["ID"] in current_applications: job["Application"] = 1
				else: job["Application"] = 0
			jobs_json = json.dumps(jobs_dict)
		except:
			return Response("Could not connect to the database", status=200, mimetype="text/html")

		return Response(jobs_json, status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")

## Applicant CV Editing page
@app.route("/applicant/cv")
def show_applicant_cv_page():
	if login_check() == "Applicant":
		return render_template("applicant_cv.html")
	return redirect("/")

# Get Applicant's Current CV
# Returns: User's CV in JSON/Text Format
@app.route("/applicant/get_cv")
def get_applicant_cv():
	account_type = login_check()
	print(account_type)
	if account_type == "Applicant":
		# GET REQUIRED SESSION PARAMETER
		user_id = session["user_id"]

		# GET USERS CURRENT CV IN JSON FORMAT
		try:
			cv_id = get_current_cv(user_id)
			cv = get_CV(cv_id)
			cv_json = jsonify_cv(cv)
		except:
			return Response("Could not connect to the database", status=200, mimetype="text/html")

		return Response(cv_json, status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")

## Saving CV Changes
# Receives: CV in JSON format
# Returns: Success/Failure for creating CV in db
@app.route("/applicant/save_cv", methods=["POST"])
def save_applicant_cv():
	if login_check() == "Applicant":
		# GET REQUIRED REQUEST PARAMETERS
		user_id = session["user_id"]
		cv = request.form.get("cv")
		cv_json = json.loads(cv)

		# SAVE USER'S CV TO DATABASE HERE
		try:
			insert_json_cv(cv_json, user_id)
		except:
			return Response("Could not connect to the database", status=200, mimetype="text/html")

		return Response("Success", status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")

# Allows Applicant to Apply for a Job
# Receives: Job_id for job being applied for
# Returns: Success/Failure
# Actions: Applies user for job with their current CV in db
@app.route("/applicant/apply_for_job", methods=["POST"])
def apply_for_job():
	if login_check() == "Applicant":
		# GET REQUIRED REQUEST PARAMETERS
		user_id = session["user_id"]
		job_id = request.form.get("job_id")

		# APPLY USER FOR JOB WITH THEIR CURRENT CV
		try:
			cv_id = get_current_cv(user_id)
			apply_job(cv_id, job_id)
		except:
			return Response("Could not connect to the database", status=200, mimetype="text/html")

		return Response("Success", status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")

# Receives applicant's answers for a given test
# Receives: job_id + question and answers
# Returns: Success/Failure
# Actions: Check user's answers and add to database with score
@app.route("/applicant/send_test_answers", methods=["POST"])
def send_test_answers():
	if login_check() == "Applicant":
		# GET REQUIRED REQUEST PARAMETERS
		user_id = session["user_id"]
		job_id = request.form.get("job_id")
		answers = request.form.get("answers")

		# SCORE TEST AND STORE IN DATABASE
		try:
			answers_json = json.loads(answers)
			cv_id = get_current_cv(user_id)
			score = score_test(answers_json, job_id, cv_id)
		except:
			return Response("Could not connect to the database", status=200, mimetype="text/html")

		return Response("Success", status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")

# Sends a test to the applicant for a given job
# Receives: job_id
# Returns: Questions with all multiple choice answers
@app.route("/applicant/get_job_test", methods=["POST"])
def get_job_test():
	if login_check() == "Applicant":
		# GET REQUIRED REQUEST PARAMETERS
		job_id = request.form.get("job_id")
		# job_id = 1

		#try:
		questions = get_test(job_id);
		questions_json = json.dumps(questions)
		# Can we get questions in this form if possible?
		# questions = [
		# 	{
		# 		"Question":question,
		# 		"Correct":correct,
		# 		"Incorrect1":incorrect1,
		# 		"Incorrect2":incorrect2,
		# 		"Incorrect3":incorrect3
		# 	}
		# ]
		#except:
		#return Response("Could not retrieve data from the database", status=200, mimetype="text/html")

		return Response(questions_json, status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")



## TEMP PAGES

# CREATE NEW ADMIN WITH PASSWORD 'TEST'
@app.route("/create_admin", methods=["GET"])
def create_test_admin():
	username=request.args.get("username")
	admin = Admin(username,'test')
	user_id = create_admin(admin)
	if user_id is None:
		return Response("ERROR", status=200, mimetype="text/html")
	return Response(str(user_id), status=200, mimetype="text/html")



## SETUP APP

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True)
