from flask import Flask, render_template, request, redirect, Response, session
from flask_cors import CORS
from flask_mail import Mail, Message
from celery import Celery
import json
import string
import random

from users import *
from ml import retrain
import os

## Session variables
# account_type : "Admin"/"Applicant"/None : Shows type of account logged in user has, or shows user isn't logged in
# user_id : Stores logged in user id from database

## NOTE: WHEN CONNECTING TO THE DATABASE, USE TRY EXCEPT BLOCKS INCASE OF DATABASE DISCONNECT OR ANY OTHER ISSUE

app = Flask(__name__, static_url_path='/static')

celery=Celery(app.name,broker='sqla+sqlite:///database.db')

CORS(app)

# Email Setup
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'PerfectCandidate.Notifications@gmail.com'
app.config['MAIL_PASSWORD'] = 'TPCGroup32'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
# PerfectCandidate.Notifications@gmail.com Password: TPCGroup32

# Send test email to self
@app.route("/testmail")
def test_mail():
	msg = Message('Hello', sender = 'PerfectCandidate.Notifications@gmail.com', recipients = ['PerfectCandidate.Notifications@gmail.com'])
	msg.body = "This is the email body"
	mail.send(msg)
	return "Sent"

# Send email with new password
def pass_mail(candidate):
	msg = Message('Hello', sender = 'PerfectCandidate.Notifications@gmail.com', recipients = candidate)
	letters = string.ascii_letters
	newpass = ''.join(random.choice(letters) for i in range(10))
	id = get_ID(candidate)
	change_pass_user(id,newpass)
	msg.body = "Your pass has been changed. New generated pass is: "+newpass
	mail.send(msg)
	return "Sent"

# Celery Task to perform in the background
@celery.task
def retrain_job_in_background(job_id,email):
	with app.app_context():
		retrain(job_id)
		msg = Message('Retraining Complete', sender = 'PerfectCandidate.Notifications@gmail.com')
		msg.add_recipient(email)
		msg.body = 'The retraining you requested has been complete. Please go to ThePerfectCandidate to view the results.'
		mail.send(msg)

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
	session.modified = True

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
	session.modified = True
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
				session.modified = True
				return Response("Success", status=200, mimetype="text/html")
		except:
			return Response("There was an issue logging you in, please try again", status=200, mimetype="text/html")

### Change staff password
# Recieves: password
@app.route("/staff/reset_password", methods=["POST"])
def reset_staff_password():
	# GET REQUIRED REQUEST PARAMETERS
	email = request.form.get("email")

	msg = Message('Hello', sender = 'PerfectCandidate.Notifications@gmail.com')
	msg.add_recipient(email)
	letters = string.ascii_letters
	newpass = "".join(random.choice(letters) for i in range(10))
	try:
		user_id = get_admin_ID(email)
		# If user with this email doesn't exist -> For security reasons don't disclose this information
		if user_id is not None:
			try:
				msg.body = "Your pass has been changed. New generated pass is: " + newpass
				msg.header = "Reset Password"
				mail.send(msg)
			except:
				# Invalid email address
				return Response("The email address entered is invalid, please try again", status=200, mimetype="text/html")
			try:
				change_pass_admin(user_id[0], newpass)
			except:
				# Issue connecting to database
				return Response("An unexpected error has occurred, if you have received an email, please ignore it and try again later", status=200, mimetype="text/html")
	except:
		return Response("Could not connect to database", status=200, mimetype="text/html")

	return Response("Success", status=200, mimetype="text/html")

## Change staff password
# Recieves: old_password, new_password
@app.route("/staff/change_password", methods=["POST"])
def change_staff_password():
	# GET REQUIRED REQUEST PARAMETERS
	user_id = session.get("user_id")
	current_password = request.form.get("current_password")
	new_password = request.form.get("new_password")
	try:
		email = get_admin(user_id)[1]
		if authenticate_admin(email, current_password) is None:
			# if None returned, password is incorrect
			return Response("The current password entered was incorrect", status=200, mimetype="text/html")
		change_pass_admin(user_id, new_password)
	except:
		return Response("There was an error changing your password, please try again", status=200, mimetype="text/html")

	return Response("Success", status=200, mimetype="text/html")

@app.route("/staff/settings")
def get_settings_page():
	if login_check() == "Admin":
		return render_template("staff_settings.html")
	return redirect("/")

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
			jobs_dict = create_staff_jobs_dictionary(jobs)
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
			return redirect("/staff/jobs")
		return render_template("staff_candidates.html",job_id=job_id)
	return redirect("/")

## Get All Candidates - Staff
# Returns: All candidates for jobs by this user in JSON/Text format
@app.route("/staff/get_candidates", methods=["POST"])
def get_candidates():
	if login_check() == "Admin":
		# GET REQUIRED REQUEST PARAMETERS
		job_id = request.form.get('job_id')
		if job_id is None:
			return Response("Could not find candidates for this job, please reload the page", status=200, mimetype="text/html")
		try:
			candidates_raw = all_complete_applications(job_id)
			candidates_dict = create_candidates_dict(candidates_raw)
			candidates_json = json.dumps(candidates_dict)
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
		job_id = request.form.get('job_id')

		# LIKE CANDIDATE FOR ROLE
		try:
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
		job_id = request.form.get('job_id')

		# DISLIKE CANDIDATE FOR ROLE
		try:
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
#			"Incorrect1":incorrect1,
# 			"Incorrect2":incorrect2,
# 			"Incorrect3":incorrect3
# 		}]
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
			job_json["Status"],
			user_id)

		questions = job_json["Questions"]
		question_number = job_json["QuestionNumber"]
		try:
			if job_id == "-1":
				new_job_id = insert_job(job)
				test_id = add_test(new_job_id,question_number)
				for question in questions:
					temp_question = Question(question["Question"],question["Correct"],question["Incorrect1"],question["Incorrect2"],question["Incorrect3"])
					add_question(test_id, temp_question)
				return Response("Success", status=200, mimetype="text/html")
			else:
				edit_job(job_id, job)
				delete_test(job_id)
				test_id = add_test(job_id,question_number)
				for question in questions:
					temp_question = Question(question["Question"],question["Correct"],question["Incorrect1"],question["Incorrect2"],question["Incorrect3"])
					add_question(test_id, temp_question)
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
			remove_job(job_id)
			delete_test(job_id)
		except:
			return Response("Could not connect to the database", status=200, mimetype="text/html")

		return Response("Success", status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")

@app.route("/staff/retrain_job", methods=["POST"])
def retrain_job():
	if login_check() == "Admin":
		# GET REQUIRED REQUEST PARAMETERS
		job_id = request.form.get("job_id")

		# Only call retrain if:
		# at least 1 cv has score 0
		# at least 1 cv has been liked/disliked

		cvs_to_score = get_untrained_cv_number(job_id)
		if cvs_to_score == 0:
			return Response("Your suggestions are currently up to date and the system does not require retraining",status=200,mimetype="text/html")

		cvs_liked_or_disliked = get_liked_disliked_cv_number(job_id)
		if cvs_liked_or_disliked == 0:
			return Response("You must provide feedback for at least one cv before you can retrain the system",status=200,mimetype="text/html")
		# Try to being ML Retraining
		try:
			# Get the current user's email to know who to send the complete email to
			user_id = session.get('user_id')
			email = get_admin(user_id)[1]

			# Begin the retraining in the background with the job_id and user's email as parameters
			task = retrain_job_in_background.apply_async(args=[job_id,email])
		except:
			return Response("Their was an issue retraining your data please try again later", status=200, mimetype="text/html")

		return Response("Success", status=200, mimetype="text/html")
	return Response("You are not logged in", status=200, mimetype="text/html")

@app.route("/staff/email_report")
def email_report():
	if login_check() == "Admin":
		# GET REQUIRED REQUEST PARAMETERS
		job_id = request.form.get("job_id")
		user_id = session["user_id"]

		# EMAIL ADMIN
		try:
			email = str(get_admin(user_id)[1])
			msg = Message('Hello', sender = 'PerfectCandidate.Notifications@gmail.com')
			msg.add_recipient(email)

			complete_applications = len(all_complete_applications(job_id))
			incomplete_applications = len(all_applications(job_id)) - complete_applications
			job_name = str(what_job(job_id)[0][1])

			msg.body = "Dear " + email + " you have " + str(complete_applications) + " completed applications and " + str(incomplete_applications) + " for the job " + job_name + ". Please review the applications at http://127.0.0.1:5000/applicant/jobs"
			msg.header = "Application Report: " + job_name
			mail.send(msg)
		except:
			return Response("Could not send email", status=200, mimetype="text/html")

		return Response("Success", status=200, mimetype="text/html")
	return Response("You are not loggen in", status=200, mimetype="text/html")

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
				session.modified = True
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
		session.modified = True
		return Response("Success", status=200, mimetype="text/html")
	except:
		return Response("There was an error creating your account, please try again", status=200, mimetype="text/html")

## Change staff password
# Recieves: password
@app.route("/applicant/reset_password", methods=["POST"])
def reset_applicant_password():
	# GET REQUIRED REQUEST PARAMETERS
	email = request.form.get("email")

	msg = Message('Hello', sender = 'PerfectCandidate.Notifications@gmail.com')
	msg.add_recipient(email)
	letters = string.ascii_letters
	newpass = "".join(random.choice(letters) for i in range(10))
	try:
		user_id = get_ID(email)
		# If user with this email doesn't exist -> For security reasons don't disclose this information
		if user_id is not None:
			try:
				msg.body = "Your pass has been changed. New generated pass is: " + newpass
				msg.header = "Reset Password"
				mail.send(msg)
			except:
				# Invalid email address
				return Response("The email address entered is invalid, please try again", status=200, mimetype="text/html")
			try:
				change_pass_user(user_id[0], newpass)
			except:
				# Issue connecting to database
				return Response("An unexpected error has occurred, if you have received an email, please ignore it and try again later", status=200, mimetype="text/html")
	except:
		return Response("Could not connect to database", status=200, mimetype="text/html")

	return Response("Success", status=200, mimetype="text/html")

## Change applicant password
# Recieves: old_password, new_password
@app.route("/applicant/change_password", methods=["POST"])
def change_applicant_password():
	# GET REQUIRED REQUEST PARAMETERS
	user_id = session.get("user_id")
	current_password = request.form.get("current_password")
	new_password = request.form.get("new_password")
	try:
		email = get_user(user_id)[0][4]
		if authenticate_user(email, current_password) is None:
			# if None returned, password is incorrect
			return Response("The current password entered was incorrect", status=200, mimetype="text/html")
		change_pass_user(user_id, new_password)
	except:
		return Response("There was an error changing your password, please try again", status=200, mimetype="text/html")

	return Response("Success", status=200, mimetype="text/html")

@app.route("/applicant/settings")
def get_applicant_settings_page():
	if login_check() == "Applicant":
		return render_template("applicant_settings.html")
	return redirect("/")

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
			jobs = get_jobs_applicant(user_id)
			jobs_dict = create_jobs_dictionary(jobs)
			complete_applications = get_completed_applications(user_id)
			incomplete_applications = get_incomplete_applications(user_id)
			for job in jobs_dict:
				job["Application"] = 0
				job["Feedback"] = 0
				if any(job["ID"] in application for application in incomplete_applications):
					job["Application"] = 1
					job["Feedback"] = 0
				else:
					for application in complete_applications:
						if job["ID"] == application[0]:
							job["Application"] = 2
							job["Feedback"] = application[1]
							break
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
			cv_id = get_cv_for_job(user_id, job_id)
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
		user_id = session["user_id"]
		job_id = request.form.get("job_id")

		#This method also needs to change the application score from -1 to 0
		try:
			questions = get_test(job_id)

			all_questions = []
			for question in questions:
				question_dict = {}
				question_dict["Question"] = question[2]
				question_dict["Correct"] = question[3]
				question_dict["Incorrect1"] = question[4]
				question_dict["Incorrect2"] = question[5]
				question_dict["Incorrect3"] = question[6]
				all_questions.append(question_dict)

			questions_json = json.dumps(all_questions)

			cv_id = get_cv_for_job(user_id,job_id)
			update_score(job_id,cv_id,0)
		except:
			return Response("Could not retrieve data from the database", status=200, mimetype="text/html")

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
