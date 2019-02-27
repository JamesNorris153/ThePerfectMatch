import sqlite3 as sql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask import g
from os import path

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

ROOT = path.dirname(path.relpath((__file__)))

class Job:

    #def __init__(self, name, description,deadline,position,location,hobbies,skills,languages,ALevels):
    def __init__(self, name, description, deadline, location, position):
        self.name = name
        self.location = location
        self.position = position
        self.deadline = deadline
        self.description = description
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

    FName = ""
    LName = ""
    degrees = []
    languages = []
    hobbies = []
    ALevels = []
    employment = []
    skills = []
    # def __init__(self, FName, LName, hobbies, languages, degrees, ALevels, employment, skills):
    #     self.FName = FName
    #     self.LName = LName
    #     self.degrees = degrees
    #     self.languages = languages
    #     self.hobbies = hobbies
    #     self.ALevels = ALevels
    #     self.employment = employment
    #     self.skills = skills

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

    # def __init__(self,university,course,grade):
    #     self.name=university
    #     self.course=course
    #     self.grade=self.grade

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
	# TODO: return user_id on creation
	# return user_id

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
		jobs_dict["Name"] = "" if (job[1] == None) else job[1]
		jobs_dict["Description"] = "" if (job[2] == None) else job[1]
		jobs_dict["Deadline"] = "" if (job[3] == None) else job[1]
		jobs_dict["Location"] = "" if (job[4] == None) else job[1]
		jobs_dict["Position"] = "" if (job[5] == None) else job[1]
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
    cur.execute('INSERT into jobs VALUES (NULL,?,?,?,?,?)',(job.name,job.description,job.deadline,job.location,job.position))
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
    cur.execute('SELECT id,password from users where email=(?)',(email,))
    passw = cur.fetchone()
    if passw == None: return None
    if bcrypt.checkpw(password, passw[1].encode("utf8")):
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
    cur.execute('SELECT grade,name from alevel_cv join alevel on alevel.id = alevel_cv.ALevel_ID WHERE CV_ID=(?)',(cvID,))
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

def close_job(jobID):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    con.execute('UPDATE jobs SET position="unavailable" where id=(?)',(jobID,))
    con.commit()
    cur.execute('UPDATE job_cv SET status=2 WHERE Job_ID=(?) AND status=0',(jobID,))
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
    cur.execute('INSERT into job_cv values (?,?,?,?)',(jobID,cvID,0,0))
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
    if bcrypt.checkpw(password.encode("utf8"),passw[1].encode("utf8")):
        con.close()
        return passw[0]
    else:
        con.close()
        return None

def create_admin(admin):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    if check_user(admin.username)==True:
        cur.execute('INSERT INTO admins VALUES (NULL,?,?)',(admin.username,bcrypt.hashpw(admin.password.encode("utf8"),bcrypt.gensalt())))
        con.commit()
    con.close()

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
    cur.execute('SELECT LName,Fname from job_cv join cvs on CV_ID=cvs.id join users on User_ID=users.id where status=0 order by score desc')
    users=cur.fetchall()
    con.close()
    return users


def insert_json_cv (form,userID):
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
