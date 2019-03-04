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

ROOT = path.dirname(path.relpath((__file__)))

class Job:

    #def __init__(self, name, description,deadline,position,location,hobbies,skills,languages,ALevels):
    def __init__(self, name, description, deadline, location, position, status):
        self.name = name
        self.location = location
        self.position = position
        self.deadline = deadline
        self.description = description
        self.status = status
        #self.hobbies = hobbies
        #self.skills = skills
        #self.languages = languages
        #self.ALevel = ALevels

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
			print(degrees)
		cv_dict["degrees"] = degrees

		languages = []
		for language in self.languages:
			languages.append(language.__dict__)
			print(languages)
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

    # def __init__(self,company,positon,length):
    #     self.name=company
    #     self.position=position
    #     self.length=self.length

class Edu:

    name = ""
    course = ""
    grade = ""

    # def __init__(self, university, course, grade):
    #     self.name=university
    #     self.course=course
    #     self.grade=self.grade

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

#Example Methods
def create_user(applicant):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    if check_mail(applicant.email)==True:
        cur.execute('INSERT INTO users VALUES (NULL,?,?,?,?)',(applicant.FName,applicant.LName,bcrypt.hashpw(applicant.password.encode("utf8"),bcrypt.gensalt()),applicant.email))
    con.commit()
    cur.execute('SELECT id FROM users WHERE email=?',(applicant.email,))
    user_id = cur.fetchone()[0]
    con.close()
    return user_id

def get_users():
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    con.close()
    return users

def get_jobs():
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM jobs')
    jobs = cur.fetchall()
    con.close()
    return jobs

def create_jobs_dictionary(jobs):
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
        all_jobs.append(jobs_dict)
    return all_jobs

# Returns true IF user doesn't exist, false otherwise
def check_mail(email):
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
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE id=(?)',(id,))
    user = cur.fetchall()
    con.close()
    return user

#ALevel/Hobbies/Languages/Skills
def get_trait_level(table, jobID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT name,level FROM {} WHERE Job_ID=(?)'.format(table),(jobID,))
    user = cur.fetchall()
    con.close()
    return user

def insert_job(job):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into jobs VALUES (NULL,?,?,?,?,?,?)',(job.name,job.description,job.deadline,job.location,job.position,job.status))
    job_id = cur.lastrowid
    con.commit()
    con.close()
    return job_id

def edit_job(job_id, job):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('UPDATE jobs SET name=(?), description=(?), deadline=(?), location=(?), position=(?), status=(?) WHERE id=(?)',(job.name, job.description, job.deadline, job.location, job.position, job.status, job_id))
    con.commit()
    con.close()

def selectAllSkills():
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

# ALevel/Hobbies/Skills/Languages
def insert_trait_dependency(table, jobID, name, level):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into {} VALUES (NULL,?,?,?)'.format(table),(jobID,name,level))
    con.commit()
    con.close()

# Degrees/Employment
def insert_special_dependency(table, jobID, name, second, level):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into {} VALUES (NULL,?,?,?,?)'.format(table),(jobID,name,second,level))
    con.commit()
    con.close()

def authenticate_user(email, password):
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
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('UPDATE job_cv SET status=(?) WHERE Job_ID=(?) AND CV_ID=(?)',(status,jobID,cvID))
    con.commit()
    con.close()

def select_status(jobID, cvID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('select status from job_cv WHERE Job_ID=(?) AND CV_ID=(?)',(jobID,cvID))
    status = cur.fetchall()[0]
    con.commit()
    con.close()
    return status

def update_score(jobID,cvID,score):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('UPDATE job_cv SET score=(?) WHERE Job_ID=(?) AND CV_ID=(?)',(score,jobID,cvID))
    con.commit()
    con.close()

def close_job(jobID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    con.execute('UPDATE jobs SET status="Unavailable" where id=(?)',(jobID,))
    con.commit()
    cur.execute('UPDATE job_cv SET status=2 WHERE Job_ID=(?) AND status=0',(jobID,))
    con.commit()
    con.close()

def reopen_job(jobID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    con.execute('UPDATE jobs SET status="Available" where id=(?)',(jobID,))
    con.commit()
    con.close()

def new_trait(jobID,trait,table):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into {} values (NULL,?,?,0)'.format(table),(jobID,trait))
    con.commit()
    con.close()

def new_degree(jobID,university,course):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into degrees values (NULL,?,?,?,?)',(jobID,university,course,0))
    con.commit()
    con.close()

def new_employment(jobID,company,position):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into employment values (NULL,?,?,?,?)',(jobID,company,position,0))
    con.commit()
    con.close()

def get_degree_level(jobID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT university,course,level FROM degrees WHERE Job_ID=(?)',(jobID,))
    user = cur.fetchall()
    con.close()
    return user

def get_employment_level(jobID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT company,position,level FROM employment WHERE Job_ID=(?)',(jobID,))
    user = cur.fetchall()
    con.close()
    return user

def get_current_cv(userID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT MAX(id) from cvs where User_ID=(?)',(userID,))
    user = cur.fetchone()[0]
    con.close()
    return user

def score_test(answers,jobID,cvID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    score=0
    for i in answers:
        cur.execute('Select answer from question_test where id=(?)',(i.id))
        correct = cur.fetchone()
        if i.answer == correct:
            score+=1
    cur.execute('Update job_cv set score=(?) where CV_ID=(?) and Job_ID=(?) and status=0',(score,cvID,jobID))
    con.commit()
    con.close()
    return score

def show_current_applications(userID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT Job_ID, CV_ID from job_cv where CV_ID in (SELECT id from cvs where User_ID=?) and status=0',(userID,))
    jobs = cur.fetchall()
    con.close()
    return jobs

def get_completed_applications(userID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT Job_ID, status from job_cv where CV_ID in (SELECT id from cvs where User_ID=?) and score>=0',(userID,))
    jobs = cur.fetchall()
    con.close()
    return jobs

def get_incomplete_applications(userID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT Job_ID, status from job_cv where CV_ID in (SELECT id from cvs where User_ID=?) and score=-1',(userID,))
    jobs = cur.fetchall()
    con.close()
    return jobs

def what_job(jobID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * from jobs where id=(?)',(jobID,))
    job = cur.fetchall()
    con.close()
    return job

def get_test(jobID):
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
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('DELETE FROM question_test WHERE Test_ID IN (SELECT id from tests WHERE Job_ID=(?))',(jobID,))
    cur.execute('DELETE from tests WHERE Job_ID=(?)',(jobID,))
    con.commit()
    con.close()


# Use the one defined bellow

# def insert_cv (form):
#     con = sql.connect(path.join(ROOT, 'test.db'))
#     cur = con.cursor()
#
#     cur.execute('Insert into cvs values (NULL,?)',(form.id))
#     cur.execute('Select max(id) from cvs')
#     max=cur.fetchone()
#
#     for i in range (1,len(form.skills)):
#         cur.execute('Select id from skills where name=(?) and Job_ID=(?)',(form.skills[i].name,),(form.jobID,))
#         id=cur.fetchone()
#         if id!=None:
#             cur.execute('INSERT into skills_cv values (?,?,?)',(id,max,form.skills[i].level))
#         else:
#             new_trait(form.jobID,form.skills[i].name,skills)
#             cur.execute('SELECT max(id) from skills')
#             id1=cur.fetchone()
#             cur.execute('INSERT into skills_cv values (?,?,?)',(id1,max,form.skills[i].level))
#
#     for i in range (1,len(form.hobbies)):
#         cur.execute('Select id from hobbies where name=(?) and Job_ID=(?)',(form.hobbies[i].name,),(form.jobID,))
#         id=cur.fetchone()
#         if id!=None:
#             cur.execute('INSERT into hobbies_cv values (?,?,?)',(id,max,form.hobbies[i].level))
#         else:
#             new_trait(form.jobID,form.hobbies[i].name,hobbies)
#             cur.execute('SELECT max(id) from hobbies')
#             id1=cur.fetchone()
#             cur.execute('INSERT into hobbies_cv values (?,?,?)',(id1,max,form.hobbies[i].level))
#
#     for i in range (1,len(form.languages)):
#         cur.execute('Select id from languages where name=(?) and Job_ID=(?)',(form.languages[i].name,),(form.jobID,))
#         id=cur.fetchone()
#         if id!=None:
#             cur.execute('INSERT into languages_cv values (?,?,?)',(id,max,form.languages[i].level))
#         else:
#             new_trait(form.jobID,form.languages[i].name,languages)
#             cur.execute('SELECT max(id) from languages')
#             id1=cur.fetchone()
#             cur.execute('INSERT into languages_cv values (?,?,?)',(id1,max,form.languages[i].level))
#
#     for i in range (1,len(form.ALevels)):
#         cur.execute('Select id from alevel where name=(?) and Job_ID=(?)',(form.ALevels[i].name,),(form.jobID,))
#         id=cur.fetchone()
#         if id!=None:
#             cur.execute('INSERT into alevel_cv values (?,?,?)',(id,max,form.ALevels[i].level))
#         else:
#             new_trait(form.jobID,form.ALevels[i].name,alevels)
#             cur.execute('SELECT max(id) from languages')
#             id1=cur.fetchone()
#             cur.execute('INSERT into languages_cv values (?,?,?)',(id1,max,form.languages[i].level))
#
#     for i in range (1,len(form.degrees)):
#         cur.execute('Select id from degrees where name=(?) and Job_ID=(?) and position=(?)',(form.degrees[i].name,),(form.jobID,),(form.degrees[i].position,))
#         id=cur.fetchone()
#         if id!=None:
#             cur.execute('INSERT into degrees_cv values (?,?,?)',(id,max,form.degrees[i].level))
#         else:
#             new_degree(form.jobID,form.degrees[i].name,form.degrees[i].position)
#             cur.execute('SELECT max(id) from degrees')
#             id1=cur.fetchone()
#             cur.execute('INSERT into degrees_cv values (?,?,?)',(id1,max,form.degrees[i].level))
#
#     for i in range (1,len(form.employment)):
#         cur.execute('Select id from employment where name=(?) and Job_ID=(?) and position=(?)',(form.employment[i].name,),(form.jobID,),(form.employment[i].course,))
#         id=cur.fetchone()
#         if id!=None:
#             cur.execute('INSERT into employment_cv values (?,?,?)',(id,max,form.employment[i].level))
#         else:
#             new_employment(form.jobID,form.employment[i].name,form.employment[i].course)
#             cur.execute('SELECT max(id) from employment')
#             id1=cur.fetchone()
#             cur.execute('INSERT into employment_cv values (?,?,?)',(id1,max,form.employment[i].level))
#
#     con.commit()
#     con.close()

def apply_job(cvID,jobID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into job_cv values (?,?,?,?)',(jobID,cvID,-1,0))
    con.commit()
    con.close()

def change_level(jobID,table,name,level):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('UPDATE {} SET level=(?) WHERE Job_ID=(?) and name=(?)'.format(table),(level,jobID,name))
    con.commit()
    con.close()

def authenticate_admin(username, password):
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
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * from job_cv join cvs on CV_ID=cvs.id join users on User_ID=users.id where status=0 and Job_ID=(?) order by score desc',(jobId,))
    users=cur.fetchall()
    con.close()
    return users

def select_cvs(jobId):
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

def insert_json_cv(form,userID):
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

def change_pass_user(userID,newpass):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('UPDATE users set password=(?) where id=(?)',(bcrypt.hashpw(newpass.encode("utf8"),bcrypt.gensalt()),userID))
    con.close()

def change_pass_admin(userID,newpass):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('UPDATE admins set password=(?) where id=(?)',(bcrypt.hashpw(newpass.encode("utf8"),bcrypt.gensalt()),userID))
    con.close()

def backup_db():
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('.backup backup_file.sq3')
    con.close()

def all_applications(jobID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('SELECT * from job_cv join cvs on CV_ID=cvs.id join users on User_ID=users.id where Job_ID=(?) order by score desc',(jobID,))
    users=cur.fetchall()
    con.close()
    return users

def add_test(jobID, question_no):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into tests values (NULL,?,?)',(jobID,question_no,))
    con.commit()
    cur.execute('SELECT id FROM tests WHERE Job_ID=?',(jobID,))
    test_id = cur.fetchone()[0]
    con.close()
    return test_id

def add_question(testID,question):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('INSERT into question_test values (NULL,?,?,?,?,?,?)',(testID,question.question,question.correct,question.incorrect1,question.incorrect2,question.incorrect3))
    con.close()


def jsonify_cv(cv):
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
