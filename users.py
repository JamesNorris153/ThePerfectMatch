import sqlite3 as sql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import json
from flask import g
from os import path

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

# The file contains methods that interact with the database as well as classes that
# represent the objects that will be retreived and uploaded to the database

ROOT = path.dirname(path.relpath((__file__)))

class Job:

    def __init__(self, name, description, deadline, location, position, status, creator):
        self.name = name
        self.location = location
        self.position = position
        self.deadline = deadline
        self.description = description
        self.status = status
        self.creator = creator

class Applicant:

    def __init__(self, FName, LName, password, email):
        self.FName = FName
        self.LName = LName
        self.password = password
        self.email = email

class Admin:

	def __init__(self, username, password):
		self.username = username
		self.password = password

class CV:

    def __init__(self):

        self.FName = ""
        self.LName = ""
        self.degrees = []
        self.languages = []
        self.hobbies = []
        self.ALevels = []
        self.employment = []
        self.skills = []

	def jsonify_cv(self):
		cv_dict = dict()

		cv_dict["FName"] = self.FName
		cv_dict["LName"] = self.LName

		degrees = []
		for degree in self.degrees:
			degrees.append(degree.__dict__)
		cv_dict["degrees"] = degrees

		languages = []
		for language in self.languages:
			languages.append(language.__dict__)
		cv_dict["languages"] = languages

		hobbies = []
		for hobby in self.hobbies:
			hobbies.append(hobby.__dict__)
		cv_dict["hobbies"] = hobbies

		ALevels = []
		for ALevel in self.ALevels:
			ALevels.append(ALevel.__dict__)
		cv_dict["alevels"] = ALevels

		employment = []
		for employ in self.employment:
			employment.append(employ.__dict__)
		cv_dict["employment"] = employment

		skills = []
		for skill in self.skills:
			skills.append(skill.__dict__)
		cv_dict["skills"] = skills

		return json.dumps(cv_dict)

class Form:

    id = 0
    degrees = []
    languages = []
    hobbies = []
    ALevels = []
    employment = []
    skills = []

    def __init__(self,id, hobbies, languages, degrees, ALevels, employment, skills):
        self.id=id
        self.degrees = degrees
        self.languages = languages
        self.hobbies = hobbies
        self.ALevels = ALevels
        self.employment = employment
        self.skills = skills


class Trait:

    name = ""
    level = 0

class Emp:

    name = ""
    position = ""
    length = ""

class Edu:

    name = ""
    course = ""
    grade = ""

class Question:

    def __init__(self,question,correct,incorrect1,incorrect2,incorrect3):
        self.question = question
        self.correct = correct
        self.incorrect1 = incorrect1
        self.incorrect2 = incorrect2
        self.incorrect3 = incorrect3

	question = ""
	correct = ""
	incorrect1 = ""
	incorrect2 = ""
	incorrect3 = ""

class Answer:

	question = ""
	answer = ""

def create_user(applicant):
    """Adds a new applicant to the db. Takes an object of type applicant as argument
    The password is hashed using bcrypt for security reasons."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    if check_mail(applicant.email)==True:
        cur.execute('INSERT INTO users VALUES (NULL,?,?,?,?)',(applicant.FName,
        applicant.LName,bcrypt.hashpw(applicant.password.encode("utf8"),bcrypt.gensalt()),applicant.email))
    con.commit()
    cur.execute('SELECT id FROM users WHERE email=?',(applicant.email,))
    user_id = cur.fetchone()[0]
    con.close()
    return user_id

def get_users():
    """Returns all the user accounts in the db."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    con.close()
    return users

def get_jobs():
    """Returns all the jobs."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM jobs')
    jobs = cur.fetchall()
    con.close()
    return jobs

def get_job_creator(job_id):
    """Returns email of the person who created the job."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT creator FROM jobs WHERE id=(?)', (job_id))
    job = cur.fetchone()
    con.close()
    return job

def get_jobs_applicant(user_id):
    """Returns all the available jobs."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('select * from jobs where status="Available" or id in (select job_id from job_cv where cv_id in (select cv_id from cvs where user_id=(?)))',(user_id,))
    jobs = cur.fetchall()
    con.close()
    return jobs

def create_jobs_dictionary(jobs):
    """Returns an array of jobs in dictionary format. Takes as input an array of
    jobs in SQL format."""
    all_jobs = []
    for job in jobs:
        jobs_dict = {}
        jobs_dict["ID"] = "" if (job[0] == None) else job[0]
        jobs_dict["Name"] = "" if (job[1] == None) else job[1]
        jobs_dict["Description"] = "" if (job[2] == None) else job[2]
        jobs_dict["Deadline"] = "" if (job[3] == None) else job[3]
        jobs_dict["Location"] = "" if (job[4] == None) else job[4]
        jobs_dict["Position"] = "" if (job[5] == None) else job[5]
        jobs_dict["Status"] = "" if (job[6] == None) else job[6]
        jobs_dict["Creator"] = "" if (job[7] == None) else job[7]
        all_jobs.append(jobs_dict)
    return all_jobs

def create_staff_jobs_dictionary(jobs):
    """Returns the jobs together with the test questions."""
    all_jobs = []
    for job in jobs:
        jobs_dict = {}
        jobs_dict["ID"] = "" if (job[0] == None) else job[0]
        jobs_dict["Name"] = "" if (job[1] == None) else job[1]
        jobs_dict["Description"] = "" if (job[2] == None) else job[2]
        jobs_dict["Deadline"] = "" if (job[3] == None) else job[3]
        jobs_dict["Location"] = "" if (job[4] == None) else job[4]
        jobs_dict["Position"] = "" if (job[5] == None) else job[5]
        jobs_dict["Status"] = "" if (job[6] == None) else job[6]
        jobs_dict["Creator"] = "" if (job[7] == None) else job[7]
        question_data = get_all_test_questions(jobs_dict["ID"])
        jobs_dict["QuestionNumber"] = question_data[0]
        jobs_dict["Questions"] = question_data[1]
        all_jobs.append(jobs_dict)
    return all_jobs

def get_all_test_questions(jobID):
    """Returns all test questions for a job in dict format."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT id,question_no from tests where Job_ID=(?)',(jobID,))
    test_data = cur.fetchone()
    if test_data is None:
        return [0,[]]
    test_id = test_data[0]
    question_no = test_data[1]
    cur.execute('SELECT question,answer,incorrect1,incorrect2,incorrect3 from question_test where Test_ID=(?)',(test_id,))
    questions=cur.fetchall()
    con.close()
    all_questions = []
    for question in questions:
        temp_dict = {}
        temp_dict["Question"] = question[0]
        temp_dict["Correct"] = question[1]
        temp_dict["Incorrect1"] = question[2]
        temp_dict["Incorrect2"] = question[3]
        temp_dict["Incorrect3"] = question[4]
        all_questions.append(temp_dict)
    return [question_no,all_questions]

def check_mail(email):
    """Used when creating a new account. Returns True if the email is not present
    in the db and False otherwise."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE email=(?)',(email,))
    users = cur.fetchall()
    con.close()
    if users!=[]:
        return False
    else:
        return True

def get_user(id):
    """Returns a specific user by id."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE id=(?)',(id,))
    user = cur.fetchall()
    con.close()
    return user

def get_admin(id):
    """Returns a specific admin by id."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM admins WHERE id=(?)',(id,))
    user = cur.fetchone()
    con.close()
    return user

def get_ID(email):
    """Returns the id of a user taking input an email."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT id from users where email=(?)',(email,))
    id = cur.fetchone()
    return id

def get_admin_ID(email):
    """Returns the id of an admin taking input an email."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT id from admins where username=(?)',(email,))
    id = cur.fetchone()
    return id

#ALevel/Hobbies/Languages/Skills
def get_trait_level(table, jobID):
    """Returns the ML level of a ALevel/Hobby/Language/Skill for a specific job.
    Takes as input a String: the table name and an int: the id of the job."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT name,level FROM {} WHERE Job_ID=(?)'.format(table),(jobID,))
    user = cur.fetchall()
    con.close()
    return user

def insert_job(job):
    """Adds a new job to the db. Takes as arguent an object of type Job."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into jobs VALUES (NULL,?,?,?,?,?,?,?)',(job.name,job.description,job.deadline,job.location,
    job.position,job.status,job.creator))
    job_id = cur.lastrowid
    con.commit()
    con.close()
    return job_id

def edit_job(job_id, job):
    """Allows an admin to change the information about a job. Takes input a job id
    and a Job object."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('UPDATE jobs SET name=(?), description=(?), deadline=(?), location=(?), position=(?), status=(?), creator=(?) WHERE id=(?)',
    (job.name, job.description, job.deadline, job.location, job.position, job.status, job.creator, job_id))
    con.commit()
    con.close()

def selectAllSkills():
    """Returns all skills."""
    skills = []
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    result = cur.execute('select * from skills where job_id=1')
    result = cur.fetchall()
    for item in result:
        skills.append(item[2])
    con.commit()
    con.close()

    return skills

def selectAllLanguages():
    """Returns all languages."""
    languages = []
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    result = cur.execute('select * from languages where job_id=1')
    result = cur.fetchall()
    for item in result:
        languages.append(item[2])
    con.commit()
    con.close()

    return languages

def selectAllAlevels():
    """Returns all ALevels."""
    Alevels = []
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    result = cur.execute('select * from ALevel where job_id=1')
    result = cur.fetchall()
    for item in result:
        Alevels.append(item[2])
    con.commit()
    con.close()

    return Alevels

def selectAllHobbies():
    """Returns all hobbies."""
    Hobbies = []
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    result = cur.execute('select * from Hobbies where job_id=1')
    result = cur.fetchall()
    for item in result:
        Hobbies.append(item[2])
    con.commit()
    con.close()

    return Hobbies

def selectAllEmployment():
    """Returns all the employment."""
    Employment = []
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    result = cur.execute('select * from Employment where job_id=1')
    result = cur.fetchall()
    for item in result:
        Employment.append(item[2])
    con.commit()
    con.close()

    return Employment

#
# def selectAllSkills(jobID):
#     """Returns all skills."""
#     skills = []
#     con = sql.connect(path.join(ROOT, 'database.db'))
#     cur = con.cursor()
#     result = cur.execute('select * from skills where job_id=(?)',(jobID,))
#     result = cur.fetchall()
#     for item in result:
#         skills.append(item[2])
#     con.commit()
#     con.close()
#
#     return skills
#
# def selectAllLanguages(jobID):
#     """Returns all languages."""
#     languages = []
#     con = sql.connect(path.join(ROOT, 'database.db'))
#     cur = con.cursor()
#     result = cur.execute('select * from languages where job_id=(?)',(jobID,))
#     result = cur.fetchall()
#     for item in result:
#         languages.append(item[2])
#     con.commit()
#     con.close()
#
#     return languages
#
# def selectAllAlevels(jobID):
#     """Returns all ALevels."""
#     Alevels = []
#     con = sql.connect(path.join(ROOT, 'database.db'))
#     cur = con.cursor()
#     result = cur.execute('select * from ALevel where job_id=(?)',(jobID,))
#     result = cur.fetchall()
#     for item in result:
#         Alevels.append(item[2])
#     con.commit()
#     con.close()
#
#     return Alevels
#
# def selectAllHobbies(jobID):
#     """Returns all hobbies."""
#     Hobbies = []
#     con = sql.connect(path.join(ROOT, 'database.db'))
#     cur = con.cursor()
#     result = cur.execute('select * from Hobbies where job_id=(?)',(jobID,))
#     result = cur.fetchall()
#     for item in result:
#         Hobbies.append(item[2])
#     con.commit()
#     con.close()
#
#     return Hobbies
#
# def selectAllEmployment(jobID):
#     """Returns all the employment."""
#     Employment = []
#     con = sql.connect(path.join(ROOT, 'database.db'))
#     cur = con.cursor()
#     result = cur.execute('select * from Employment where job_id=(?)',(jobID,))
#     result = cur.fetchall()
#     for item in result:
#         Employment.append(item[2])
#     con.commit()
#     con.close()
#
#     return Employment

# ALevel/Hobbies/Skills/Languages
def insert_trait_dependency(table, jobID, name, level):
    """Adds a link between a certain ALevel/Hobby/Skill/Language and the likelihood
    of its possessor to get a specific job. Takes as input the table name, the job id
    the name of the trait and the level of the link."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into {} VALUES (NULL,?,?,?)'.format(table),(jobID,name,level))
    con.commit()
    con.close()

# Degrees/Employment
def insert_special_dependency(table, jobID, name, second, level):
    """Adds a link between a certain Degrees/Employment and the likelihood
    of its possessor to get a specific job. Takes as input the table name, the job id
    the name of the trait, the position/degree and the level of the link."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into {} VALUES (NULL,?,?,?,?)'.format(table),(jobID,name,second,level))
    con.commit()
    con.close()

def authenticate_user(email, password):
    """Checks if the inputed password matches the one in the db to permit access
    to a user account."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT id, password from users where email=(?)',(email,))
    passw = cur.fetchone()
    if passw == None: return None
    if bcrypt.checkpw(password.encode("utf8"),str(passw[1])):
        con.close()
        return passw[0]
    else:
        con.close()
        return None

def get_CV(cvID):
    """Returns a cv based on a cv id. A CV object is formed and filled with info from
    all the tables."""
    info = CV()
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT User_ID from cvs WHERE id=(?)',(cvID,))
    user = cur.fetchone()[0]
    cur.execute('SELECT FName,LName from users where id=(?)',(user,))
    result = cur.fetchone()
    info.FName = result[0]
    info.LName = result[1]
    cur.execute('SELECT grade,name from alevel_cv join alevel on alevel.id = alevel_cv.CV_ID WHERE ALevel_ID=(?)',(cvID,))
    result = cur.fetchall()
    for row in result:
        put = Trait()
        put.name = row[1]
        put.level = row[0]
        info.ALevels.append(put)
    cur.execute('SELECT expertise,name from skills_cv join skills on skills.id = skills_cv.Skills_ID WHERE CV_ID=(?)',(cvID,))
    result = cur.fetchall()
    for row in result:
        put = Trait()
        put.name = row[1]
        put.level = row[0]
        info.skills.append(put)
    cur.execute('SELECT expertise,name from language_cv join languages on languages.id = language_cv.Language_ID WHERE CV_ID=(?)',(cvID,))
    result = cur.fetchall()
    for row in result:
        put = Trait()
        put.name = row[1]
        put.level = row[0]
        info.languages.append(put)
    cur.execute('SELECT interest,name from hobby_cv join hobbies on hobbies.id = hobby_cv.Hobby_ID WHERE CV_ID=(?)',(cvID,))
    result = cur.fetchall()
    for row in result:
        put = Trait()
        put.name = row[1]
        put.level = row[0]
        info.hobbies.append(put)
    cur.execute('SELECT company,position,length from employment_cv join employment on employment.id = employment_cv.Employment_ID WHERE CV_ID=(?)',(cvID,))
    result = cur.fetchall()
    for row in result:
        put = Emp()
        put.name = row[0]
        put.position = row[1]
        put.length = row[2]
        info.employment.append(put)
    cur.execute('SELECT university,course,grade from degree_cv join degrees on degrees.id = degree_cv.Degree_ID WHERE CV_ID=(?)',(cvID,))
    result = cur.fetchall()
    for row in result:
        put = Edu()
        put.name = row[0]
        put.course = row[1]
        put.grade = row[2]
        info.degrees.append(put)
    con.close()
    return info

def update_status(jobID,cvID,status):
    """Changes the statu of an application."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('UPDATE job_cv SET status=(?) WHERE Job_ID=(?) AND CV_ID=(?)',(status,jobID,cvID))
    con.commit()
    con.close()

def select_status(jobID, cvID):
    """Returns the status of an applicaton."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('select status from job_cv WHERE Job_ID=(?) AND CV_ID=(?)',(jobID,cvID))
    status = cur.fetchall()[0]
    con.commit()
    con.close()
    return status

def update_score(jobID,cvID,score):
    """Change the score of an application."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('UPDATE job_cv SET score=(?) WHERE Job_ID=(?) AND CV_ID=(?)',(score,jobID,cvID))
    con.commit()
    con.close()

def close_job(jobID):
    """Makes the job unavailable and rejects all candidates that were not dealt with."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    con.execute('UPDATE jobs SET status="Unavailable" where id=(?)',(jobID,))
    con.commit()
    cur.execute('UPDATE job_cv SET status=2 WHERE Job_ID=(?) AND status=0',(jobID,))
    con.commit()
    con.close()

def remove_job(jobID):
    """Deletes a job from the db."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('DELETE FROM jobs WHERE id=(?)', (jobID))
    con.commit()
    con.close()

def reopen_job(jobID):
    """Makes an Unavailable job available."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    con.execute('UPDATE jobs SET status="Available" where id=(?)',(jobID,))
    con.commit()
    con.close()

# WE NEED TO CHECK DESCRIPTION FOR IF TRAIT EXISTS -> SET TO 1
def new_trait(jobID,trait,table):
    """Links a certain attribute to the likeliood of being accepted for a specific
    job. Usable for ALevels/Skills/Hobbies/Languages."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into {} values (NULL,?,?,0)'.format(table),(jobID,trait))
    con.commit()
    con.close()

# def new_trait(jobID,trait,table):
#     """Links a certain attribute to the likeliood of being accepted for a specific
#     job. Usable for ALevels/Skills/Hobbies/Languages."""
#     con = sql.connect(path.join(ROOT, 'database.db'))
#     cur = con.cursor()
#     value = 0
#     if job_id != -1:
#         description = get_description(jobID)
#         print(description)
#         if trait in description:
#             print('TRAIT FOUND')
#             value = 1
#     cur.execute('INSERT into {} values (NULL,?,?,?)'.format(table),(jobID,trait,value,))
#     con.commit()
#     con.close()

def get_description(jobID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT description from jobs where id=(?)',(jobID,))
    description = cur.fetchone()[0]
    con.close()
    return description

def new_degree(jobID,university,course):
    """Links a certain degree to the likeliood of being accepted for a specific
    job."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into degrees values (NULL,?,?,?,?)',(jobID,university,course,0))
    con.commit()
    con.close()

def new_employment(jobID,company,position):
    """Links a certain employment to the likeliood of being accepted for a specific
    job."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into employment values (NULL,?,?,?,?)',(jobID,company,position,0))
    con.commit()
    con.close()

def get_degree_level(jobID):
    """Returns the level of a degree for a job."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT university,course,level FROM degrees WHERE Job_ID=(?)',(jobID,))
    user = cur.fetchall()
    con.close()
    return user

def get_employment_level(jobID):
    """Returns the level of an employment for a job."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT company,position,level FROM employment WHERE Job_ID=(?)',(jobID,))
    user = cur.fetchall()
    con.close()
    return user

def get_current_cv(userID):
    """Selects the last CV a user has uploaded."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT MAX(id) from cvs where User_ID=(?)',(userID,))
    user = cur.fetchone()[0]
    con.close()
    return user

def select_testScore(jobID, cvID):
    """Returns the test score of an applicant."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('select testScore from job_cv WHERE Job_ID=(?) AND CV_ID=(?)',(jobID,cvID))
    testScore = cur.fetchall()[0]
    con.commit()
    con.close()
    return testScore

def score_test(answers,job_id,cv_id):
    """Marks the answers of an applicant and stores the result in the db. Also returns
    the score."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    score=0
    for i in answers:
        cur.execute('Select answer from question_test where question=(?) and test_id in (SELECT id from tests where job_id=(?))',(i["Question"],job_id))
        correct = cur.fetchone()[0]
        if i["Answer"] == correct:
            score+=1
    cur.execute('Update job_cv set testScore=(?) where CV_ID=(?) and Job_ID=(?) and status=0',(score,cv_id,job_id))
    con.commit()
    con.close()
    return score

def show_current_applications(userID):
    """Shows the applications in process for a specific user."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT Job_ID, CV_ID from job_cv where CV_ID in (SELECT id from cvs where User_ID=?) and status=0',(userID,))
    jobs = cur.fetchall()
    con.close()
    return jobs

def get_completed_applications(userID):
    """Returns the completed applications for a user."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT Job_ID, status from job_cv where CV_ID in (SELECT id from cvs where User_ID=?) and score>=0',(userID,))
    jobs = cur.fetchall()
    con.close()
    return jobs

def get_incomplete_applications(userID):
    """Returns the application for which the user has to take the test."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT Job_ID, status from job_cv where CV_ID in (SELECT id from cvs where User_ID=?) and score=-1',(userID,))
    jobs = cur.fetchall()
    con.close()
    return jobs

def what_job(jobID):
    """Returns all the information about a job based on its id."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * from jobs where id=(?)',(jobID,))
    job = cur.fetchall()
    con.close()
    return job

def get_test(jobID):
    """Returns 10 randomly selected questions from a randomly selected test for a specific job."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT id,question_no from tests where Job_ID=(?)',(jobID,))
    test_data = cur.fetchone()
    test_id = test_data[0]
    question_no = test_data[1]
    cur.execute('SELECT * from question_test where Test_ID=(?) order by random() limit (?)',(test_id,question_no,))
    questions=cur.fetchall()
    con.close()
    return questions

def delete_test(jobID):
    """Removes a test from the db."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('DELETE FROM question_test WHERE Test_ID IN (SELECT id from tests WHERE Job_ID=(?))',(jobID,))
    cur.execute('DELETE from tests WHERE Job_ID=(?)',(jobID,))
    con.commit()
    con.close()

def apply_job(cvID,jobID):
    """Adds an entry marking a user applying to a role in the db."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into job_cv values (?,?,?,?,?)',(jobID,cvID,-1,0,0))
    con.commit()
    con.close()

# NEEDS TO: Get all skills/alevels/etc from cv -> link them to job specific ids
# CURRENTLY all skills/alevels/etc. are in skills/alevels/etc. table with jobid -1
# Check if job has same skills/alevels in table already -> if so, update alevel_id to one for job
# If not, create row in table with job_id new and level=0 or 1 depending on whether it appears in description

# Skills
# skills_ids = select skills_id from skills_cv where cv_id=cvID // GETS ALL SKILL IDS IN CV (JOB ID = -1)
#
#

# select skills_id from skills_cv where cv_id=cvID
# select id from skills where job_id=jobID
# def apply_job(cvID,jobID):
#     """Adds an entry marking a user applying to a role in the db."""
#     con = sql.connect(path.join(ROOT, 'database.db'))
#     cur = con.cursor()
#
#     cur.execute('SELECT skills_id from skills_cv where cv_id=(?)',(cvID,))
#     skill_ids = cur.fetchall()
#     for skill in skill_ids:
#         skill_id = skill[0]
#         cur.execute('SELECT id FROM skills WHERE name=(SELECT name FROM skills WHERE id=(?)) AND job_id=(?)',(skill_id,jobID,))
#         data = cur.fetchone()
#         if data == None:
#             # Skill does not exist for this job
#             cur.execute('INSERT INTO skills VALUES (NULL,?,?,?)',(jobID,name,level,))
#         else:
#             # Skill exists for this job
#             job_skill_id = data[0]
#
#     # cur.execute('UPDATE job')
#     # cur.execute('INSERT into job_cv values (?,?,?,?,?)',(jobID,cvID,-1,0,0))
#     # con.commit()
#     con.close()

def change_level(jobID,table,name,level):
    """Modifies the level of a certain attribute in relation to a job."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('UPDATE {} SET level=(?) WHERE Job_ID=(?) and name=(?)'.format(table),(level,jobID,name))
    con.commit()
    con.close()

def authenticate_admin(username, password):
    """Checks the password in the database to match the one inserted. Is used in admin
    authenticaion."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT id,password from admins where username=(?)',(username,))
    passw = cur.fetchone()
    if passw == None: return None
    if bcrypt.checkpw(password.encode("utf8"),str(passw[1])):
        con.close()
        return passw[0]
    else:
        con.close()
        return None

def create_admin(admin):
    """Create an admin account."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    user_id = None
    if check_user(admin.username)==True:
        cur.execute('INSERT INTO admins VALUES (NULL,?,?)',(admin.username,bcrypt.hashpw(admin.password.encode("utf8"),bcrypt.gensalt())))
        con.commit()
        cur.execute('SELECT id FROM admins WHERE username=?',(admin.username,))
        user_id = cur.fetchone()[0]
    con.close()
    return user_id

def check_user(username):
    """Check if a username is taken. Used in admin creation."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM admins WHERE username=(?)',(username,))
    users = cur.fetchall()
    con.close()
    if users!=[]:
        return False
    else:
        return True

def show_best_candidates(jobId):
    """Displays the best candidates for a specific job ordered by their scores."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * from job_cv join cvs on CV_ID=cvs.id join users on User_ID=users.id where status=0 and score!=-1 and Job_ID=(?) order by score desc',(jobId,))
    users=cur.fetchall()
    con.close()
    return users

def select_cvs(jobId):
    """Return all the CV that were used to apply to a certain job."""
    cvID = []
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT cv_id from job_cv where job_id=(?)',(jobId,))
    ids = cur.fetchall()
    for item in ids:
        cvID.append(item)
    con.commit()
    con.close()
    return cvID

def select_cvs_completed(jobId):
    """Return all the CV that were used to apply to a certain job in completed applications (completed test)."""
    cvID = []
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT cv_id from job_cv where job_id=(?) and score>=0',(jobId,))
    ids = cur.fetchall()
    for item in ids:
        cvID.append(item)
    con.commit()
    con.close()
    return cvID

def insert_json_cv(form,userID):
    """Allows users to insert a CV."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()

    cur.execute('Insert into cvs values (NULL,?)',(userID,))
    con.commit()
    cur.execute('Select max(id) from cvs')
    max=cur.fetchone()

    for i in range (0,len(form["Skills"])):
        cur.execute('Select id from skills where name=(?) and Job_ID=1',(form["Skills"][i]["Skill"],))
        id=cur.fetchone()
        if id!=None:
            cur.execute('INSERT into skills_cv values (?,?,?)',(id[0],max[0],int(form["Skills"][i]["Expertise"])))
            con.commit()
        else:
            new_trait(1,form["Skills"][i]["Skill"],'skills')
            cur.execute('SELECT max(id) from skills')
            id1=cur.fetchone()
            cur.execute('INSERT into skills_cv values (?,?,?)',(id1[0],max[0],form["Skills"][i]["Expertise"]))
            con.commit()

    for i in range (0,len(form["Hobbies"])):
        cur.execute('Select id from hobbies where name=(?) and Job_ID=1',(form["Hobbies"][i]["Name"],))
        id=cur.fetchone()
        if id!=None:
            cur.execute('INSERT into hobby_cv values (?,?,?)',(id[0],max[0],form["Hobbies"][i]["Interest"]))
            con.commit()
        else:
            new_trait(1,form["Hobbies"][i]["Name"],'hobbies')
            cur.execute('SELECT max(id) from hobbies')
            id1=cur.fetchone()
            cur.execute('INSERT into hobby_cv values (?,?,?)',(id1[0],max[0],form["Hobbies"][i]["Interest"]))
            con.commit()

    for i in range (0,len(form["Languages Known"])):
        cur.execute('Select id from languages where name=(?) and Job_ID=1',(form["Languages Known"][i]["Language"],))
        id=cur.fetchone()
        if id!=None:
            cur.execute('INSERT into language_cv values (?,?,?)',(id[0],max[0],form["Languages Known"][i]["Expertise"]))
            con.commit()
        else:
            new_trait(1,form["Languages Known"][i]["Language"],'languages')
            cur.execute('SELECT max(id) from languages')
            id1=cur.fetchone()
            cur.execute('INSERT into language_cv values (?,?,?)',(id1[0],max[0],form["Languages Known"][i]["Expertise"]))
            con.commit()

    for i in range (0,len(form["A-Level Qualifications"])):
        cur.execute('Select id from alevel where name=(?) and Job_ID=1',(form["A-Level Qualifications"][i]["Subject"],))
        id=cur.fetchone()
        if id!=None:
            cur.execute('INSERT into alevel_cv values (?,?,?)',(id[0],max[0],form["A-Level Qualifications"][i]["Grade"]))
            con.commit()
        else:
            new_trait(1,form["A-Level Qualifications"][i]["Subject"],'alevel')
            cur.execute('SELECT max(id) from alevel')
            id1=cur.fetchone()
            cur.execute('INSERT into alevel_cv values (?,?,?)',(id1[0],max[0],form["A-Level Qualifications"][i]["Grade"]))
            con.commit()

    cur.execute('Select id from degrees where university=(?) and Job_ID=1 and course=(?)',(form["University Attended"],form["Degree Qualification"]))
    id=cur.fetchone()
    if id!=None:
        cur.execute('INSERT into degree_cv values (?,?,?)',(id[0],max[0],form["Degree Level"]))
        con.commit()
    else:
        new_degree(1,form["University Attended"],form["Degree Qualification"])
        cur.execute('SELECT max(id) from degrees')
        id1=cur.fetchone()
        cur.execute('INSERT into degree_cv values (?,?,?)',(id1[0],max[0],form["Degree Level"]))
        con.commit()

    for i in range (0,len(form["Previous Employment"])):
        cur.execute('Select id from employment where company=(?) and Job_ID=1 and position=(?)',(form["Previous Employment"][i]["Company"],form["Previous Employment"][i]["Position"]))
        id=cur.fetchone()
        if id!=None:
            cur.execute('INSERT into employment_cv values (?,?,?)',(id[0],max[0],form["Previous Employment"][i]["Length of Employment"]))
            con.commit()
        else:
            new_employment(1,form["Previous Employment"][i]["Company"],form["Previous Employment"][i]["Position"])
            cur.execute('SELECT max(id) from employment')
            id1=cur.fetchone()
            cur.execute('INSERT into employment_cv values (?,?,?)',(id1[0],max[0],form["Previous Employment"][i]["Length of Employment"]))
            con.commit()

    con.close()

# def insert_json_cv(form,userID):
#     """Allows users to insert a CV."""
#     con = sql.connect(path.join(ROOT, 'database.db'))
#     cur = con.cursor()
#
#     cur.execute('Insert into cvs values (NULL,?)',(userID,))
#     con.commit()
#     cur.execute('Select max(id) from cvs')
#     max=cur.fetchone()
#
#     for i in range (0,len(form["Skills"])):
#         cur.execute('Select id from skills where name=(?) and Job_ID=-1',(form["Skills"][i]["Skill"],))
#         id=cur.fetchone()
#         if id!=None:
#             cur.execute('INSERT into skills_cv values (?,?,?)',(id[0],max[0],int(form["Skills"][i]["Expertise"])))
#             con.commit()
#         else:
#             new_trait(-1,form["Skills"][i]["Skill"],'skills')
#             cur.execute('SELECT max(id) from skills')
#             id1=cur.fetchone()
#             cur.execute('INSERT into skills_cv values (?,?,?)',(id1[0],max[0],form["Skills"][i]["Expertise"]))
#             con.commit()
#
#     for i in range (0,len(form["Hobbies"])):
#         cur.execute('Select id from hobbies where name=(?) and Job_ID=-1',(form["Hobbies"][i]["Name"],))
#         id=cur.fetchone()
#         if id!=None:
#             cur.execute('INSERT into hobby_cv values (?,?,?)',(id[0],max[0],form["Hobbies"][i]["Interest"]))
#             con.commit()
#         else:
#             new_trait(-1,form["Hobbies"][i]["Name"],'hobbies')
#             cur.execute('SELECT max(id) from hobbies')
#             id1=cur.fetchone()
#             cur.execute('INSERT into hobby_cv values (?,?,?)',(id1[0],max[0],form["Hobbies"][i]["Interest"]))
#             con.commit()
#
#     for i in range (0,len(form["Languages Known"])):
#         cur.execute('Select id from languages where name=(?) and Job_ID=-1',(form["Languages Known"][i]["Language"],))
#         id=cur.fetchone()
#         if id!=None:
#             cur.execute('INSERT into language_cv values (?,?,?)',(id[0],max[0],form["Languages Known"][i]["Expertise"]))
#             con.commit()
#         else:
#             new_trait(-1,form["Languages Known"][i]["Language"],'languages')
#             cur.execute('SELECT max(id) from languages')
#             id1=cur.fetchone()
#             cur.execute('INSERT into language_cv values (?,?,?)',(id1[0],max[0],form["Languages Known"][i]["Expertise"]))
#             con.commit()
#
#     for i in range (0,len(form["A-Level Qualifications"])):
#         cur.execute('Select id from alevel where name=(?) and Job_ID=-1',(form["A-Level Qualifications"][i]["Subject"],))
#         id=cur.fetchone()
#         if id!=None:
#             cur.execute('INSERT into alevel_cv values (?,?,?)',(id[0],max[0],form["A-Level Qualifications"][i]["Grade"]))
#             con.commit()
#         else:
#             new_trait(-1,form["A-Level Qualifications"][i]["Subject"],'alevel')
#             cur.execute('SELECT max(id) from alevel')
#             id1=cur.fetchone()
#             cur.execute('INSERT into alevel_cv values (?,?,?)',(id1[0],max[0],form["A-Level Qualifications"][i]["Grade"]))
#             con.commit()
#
#     cur.execute('Select id from degrees where university=(?) and Job_ID=-1 and course=(?)',(form["University Attended"],form["Degree Qualification"]))
#     id=cur.fetchone()
#     if id!=None:
#         cur.execute('INSERT into degree_cv values (?,?,?)',(id[0],max[0],form["Degree Level"]))
#         con.commit()
#     else:
#         new_degree(-1,form["University Attended"],form["Degree Qualification"])
#         cur.execute('SELECT max(id) from degrees')
#         id1=cur.fetchone()
#         cur.execute('INSERT into degree_cv values (?,?,?)',(id1[0],max[0],form["Degree Level"]))
#         con.commit()
#
#     for i in range (0,len(form["Previous Employment"])):
#         cur.execute('Select id from employment where company=(?) and Job_ID=-1 and position=(?)',(form["Previous Employment"][i]["Company"],form["Previous Employment"][i]["Position"]))
#         id=cur.fetchone()
#         if id!=None:
#             cur.execute('INSERT into employment_cv values (?,?,?)',(id[0],max[0],form["Previous Employment"][i]["Length of Employment"]))
#             con.commit()
#         else:
#             new_employment(-1,form["Previous Employment"][i]["Company"],form["Previous Employment"][i]["Position"])
#             cur.execute('SELECT max(id) from employment')
#             id1=cur.fetchone()
#             cur.execute('INSERT into employment_cv values (?,?,?)',(id1[0],max[0],form["Previous Employment"][i]["Length of Employment"]))
#             con.commit()
#
#     con.close()

def change_pass_user(userID,newpass):
    """Updates the password of a user in the database."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('UPDATE users set password=(?) where id=(?)',(bcrypt.hashpw(newpass.encode("utf8"),bcrypt.gensalt()),userID))
    con.commit()
    con.close()

def change_pass_admin(userID,newpass):
    """Updates the password of an admin in the db."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('UPDATE admins set password=(?) where id=(?)',(bcrypt.hashpw(newpass.encode("utf8"),bcrypt.gensalt()),userID))
    con.commit()
    con.close()

def backup_db():
    """Used to backup the entire db."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('.backup backup_file.sq3')
    con.close()

def all_applications(jobID):
    """All the applicants for a certain position."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT user_id,fname,lname,email,score,cv_id,status from job_cv join cvs on CV_ID=cvs.id join users on User_ID=users.id where Job_ID=(?) order by score desc',(jobID,))
    users=cur.fetchall()
    con.close()
    return users

def all_complete_applications(jobID):
    """All the applicants who have finished their application for a certain position."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT user_id,fname,lname,email,score,cv_id,status from job_cv join cvs on CV_ID=cvs.id join users on User_ID=users.id where Job_ID=(?) and score>=0 order by status asc, score desc',(jobID,))
    users=cur.fetchall()
    con.close()
    return users

def create_candidates_dict(candidates_raw):
    """Transforms a list of candidates in SQL format into a dict format."""
    all_candidates = []
    for candidate in candidates_raw:
        candidate_dict = {}
        candidate_dict["ID"] = "" if (candidate[0] == None) else candidate[0]
        candidate_dict["First Name"] = "" if (candidate[1] == None) else candidate[1]
        candidate_dict["Last Name"] = "" if (candidate[2] == None) else candidate[2]
        candidate_dict["Email"] = "" if (candidate[3] == None) else candidate[3]
        candidate_dict["Score"] = "" if (candidate[4] == None) else candidate[4]
        candidate_dict["CVID"] = "" if (candidate[5] == None) else candidate[5]
        candidate_dict["Status"] = "" if (candidate[6] == None) else candidate[6]
        all_candidates.append(candidate_dict)
    return all_candidates

def add_test(jobID, question_no):
    """Permits the creation of a new test."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into tests values (NULL,?,?)',(jobID,question_no,))
    con.commit()
    cur.execute('SELECT id FROM tests WHERE Job_ID=?',(jobID,))
    test_id = cur.fetchone()[0]
    con.close()
    return test_id

def add_question(testID,question):
    """Adds a new question to a test."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into question_test values (NULL,?,?,?,?,?,?)',(testID,question.question,question.correct,question.incorrect1,question.incorrect2,question.incorrect3))
    con.commit()
    con.close()

def get_cv_for_job(user_id,job_id):
    """Gets the cv with wich a specific user applied to a role."""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT cv_id FROM job_cv WHERE job_id=(?) and cv_id in (select id from cvs where user_id=(?))',(job_id,user_id,))
    cv_id = cur.fetchone()[0]
    con.close()
    return cv_id

def jsonify_cv(cv):
    """Transforms a CV in dict format from SQL format."""
    cv_dict = dict()

    cv_dict["FName"] = cv.FName
    cv_dict["LName"] = cv.LName

    degrees = []
    for degree in cv.degrees:
        degrees.append(degree.__dict__)
    cv_dict["degrees"] = degrees

    languages = []
    for language in cv.languages:
        languages.append(language.__dict__)
    cv_dict["languages"] = languages

    hobbies = []
    for hobby in cv.hobbies:
        hobbies.append(hobby.__dict__)
    cv_dict["hobbies"] = hobbies

    ALevels = []
    for ALevel in cv.ALevels:
        ALevels.append(ALevel.__dict__)
    cv_dict["alevels"] = ALevels

    employment = []
    for employ in cv.employment:
        employment.append(employ.__dict__)
    cv_dict["employment"] = employment

    skills = []
    for skill in cv.skills:
        skills.append(skill.__dict__)
    cv_dict["skills"] = skills

    return json.dumps(cv_dict)


def get_untrained_cv_number(job_id):
    """Gets the number of cvs for a job that have not been used in training"""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT COUNT(cv_id) FROM job_cv WHERE job_id=(?) and status=0 and score!=-1',(job_id,))
    cv_num = cur.fetchone()[0]
    con.close()
    return cv_num

def get_liked_disliked_cv_number(job_id):
    """Gets the number of cvs for a job that have been liked or disliked"""
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT COUNT(cv_id) FROM job_cv WHERE job_id=(?) and status!=0',(job_id,))
    cv_num = cur.fetchone()[0]
    con.close()
    return cv_num
