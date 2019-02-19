import sqlite3 as sql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import g
from os import path

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

ROOT = path.dirname(path.relpath((__file__)))

class Job:

    def __init__(self, name, description,deadline,position,location,hobbies,skills,languages,ALevels):
        self.name = name
        self.location = location
        self.position = position
        self.deadline = deadline
        self.description = description
        self.hobbies = hobbies
        self.skills = skills
        self.languages = languages
        self.ALevel = ALevels


class Applicant:

    def __init__(self, FName, LName, password, email):
        self.FName = FName
        self.LName = LName
        self.password = password
        self.email = email

class CV:

    FName = ""
    LName = ""
    degrees = []
    languages = []
    hobbies = []
    ALevels = []
    employment = []
    skills = []
    def __init__(self, FName, LName, hobbies, languages, degrees, ALevels, employment, skills):
        self.FName = FName
        self.LName = LName
        self.degrees = degrees
        self.languages = languages
        self.hobbies = hobbies
        self.ALevels = ALevels
        self.employment = employment
        self.skills = skills

class Form:

    id = 0
    degrees = []
    languages = []
    hobbies = []
    ALevels = []
    employment = []
    skills = []


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
    grade = 0

#Example Methods
def create_user(applicant):
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    if check_mail(applicant.email)==True:
        cur.execute('INSERT INTO users VALUES (NULL,?,?,?,?)',(applicant.FName,applicant.LName,bcrypt.generate_password_hash(applicant.password),applicant.email))
    con.commit()
    con.close()

def get_users():
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    con.close()
    return users

def get_jobs():
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM jobs')
    users = cur.fetchall()
    con.close()
    return users

def check_mail(email):
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE email=(?)',(email,))
    users = cur.fetchall()
    con.close()
    if users!=[]:
        return False
    else:
        return True

def get_user(id):
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE id=(?)',(id,))
    user = cur.fetchall()
    con.close()
    return user

#ALevel/Hobbies/Languages/Skills
def get_trait_level(table, jobID):
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('SELECT name,level FROM (?) WHERE Job_ID=(?)',(table,),(jobID,))
    user = cur.fetchall()
    con.close()
    return user

def insert_job(job):
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('INSERT into jobs VALUES (NULL,?,?,?,?,?)',(job.name,job.description,job.deadline,job.location,job.position))
    cur.execute('Select Max(id) from jobs')
    max = cur.fetchone()
    for i in range(1,len(hobbies)):
        cur.execute('INSERT into hobbbies values (NULL,?,?,?)',(max,hobbies[i].name,hobbies[i].level))
    for i in range(1,len(languages)):
        cur.execute('INSERT into languages values (NULL,?,?,?)',(max,languages[i].name,languages[i].level))
    for i in range(1,len(skills)):
        cur.execute('INSERT into skills values (NULL,?,?,?)',(max,skills[i].name,skills[i].level))
    for i in range(1,len(ALevel)):
        cur.execute('INSERT into alevel values (NULL,?,?,?)',(max,ALevel[i].name,ALevel[i].level))
    con.commit()
    con.close()

def authenticate_user(email, password):
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('SELECT password from users where email=(?)',(email,))
    passw = cur.fetchone()
    if bcrypt.check_password_hash(passw, password):
        con.close()
        return True
    else:
        con.close()
        return False

def get_CV(cvID):
    info = CV()
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('SELECT unique(User_ID) from cvs WHERE id=(?)',(cvID,))
    user = cur.fetchone()
    result=cur.execute('SELECT FName,LName from users where id=(?)',(user,))
    info.FName = result['FName']
    info.LName = result['LName']
    cur.execute('SELECT grade,name from alevel_cv join alevel on alevel.id = alevel_cv.ALevel_ID WHERE CV_ID=(?)',(cvID,))
    result = cur.fetchall()
    for row in result:
        put = Trait()
        put.name = row['name']
        put.level = row['grade']
        info.ALevels.append(put)
    cur.execute('SELECT expertise,name from skills_cv join skills on skills.id = skills_cv.Skills_ID WHERE CV_ID=(?)',(cvID,))
    result = cur.fetchall()
    for row in result:
        put = Trait()
        put.name = row['name']
        put.level = row['expertise']
        info.skills.append(put)
    cur.execute('SELECT expertise,name from languages_cv join languages on languages.id = languages_cv.Language_ID WHERE CV_ID=(?)',(cvID,))
    result = cur.fetchall()
    for row in result:
        put = Trait()
        put.name = row['name']
        put.level = row['expertise']
        info.languages.append(put)
    cur.execute('SELECT interest,name from hobby_cv join hobbbies on hobbies.id = hobby_cv.Hobby_ID WHERE CV_ID=(?)',(cvID,))
    result = cur.fetchall()
    for row in result:
        put = Trait()
        put.name = row['name']
        put.level = row['expertise']
        info.hobbies.append(put)
    cur.execute('SELECT company,position,length from employment_cv join employment on employment.id = employment_cv.Employment_ID WHERE CV_ID=(?)',(cvID,))
    result = cur.fetchall()
    for row in result:
        put = Emp()
        put.name = row['company']
        put.position = row['position']
        put.length = row['length']
        info.employment.append(put)
    cur.execute('SELECT university,course,grade from degree_cv join degrees on degrees.id = degrees_cv.Degree_ID WHERE CV_ID=(?)',(cvID,))
    result = cur.fetchall()
    for row in result:
        put = Edu()
        put.name = row['university']
        put.course = row['course']
        put.grade = row['grade']
        info.degrees.append(put)
    con.close()
    return info

def update_status(jobID,cvID,status):
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('UPDATE job_cv SET status=(?) WHERE Job_ID=(?) AND CV_ID=(?)',(status,),(jobID,),(cvID,))
    con.commit()
    con.close()

def new_traits(jobID,traits,table):
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('INSERT into (?) values (NULL,?,?,?)',(table,),(jobID,traits,0))
    con.commit()
    con.close()

def new_degree(jobID,university,course):
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('INSERT into degrees values (NULL,?,?,?,?)',(jobID,university,course,0))
    con.commit()
    con.close()

def new_employment(jobID,company,position):
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('INSERT into degrees values (NULL,?,?,?,?)',(jobID,company,position,0))
    con.commit()
    con.close()

def get_degree_level(table, jobID):
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('SELECT university,course,level FROM degrees WHERE Job_ID=(?)',(jobID,))
    user = cur.fetchall()
    con.close()
    return user

def get_university_level(table, jobID):
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('SELECT company,position,level FROM employment WHERE Job_ID=(?)',(jobID,))
    user = cur.fetchall()
    con.close()
    return user

def insert_cv (form):
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()

    cur.execute('Insert into cvs values (NULL,?)',(form.id))
    cur.execute('Select max(id) from cvs')
    max=cur.fetchone()

    for i in range (1,len(form.skills)):
        cur.execute('Select id from skills where name=(?) and Job_ID=(?)',(form.skills[i].name,),(form.jobID,))
        id=cur.fetchone()
        if id!=None:
            cur.execute('INSERT into skills_cv values (?,?,?)',(id,max,form.skills[i].level))
        else:
            new_traits(form.jobID,form.skills[i].name,skills)
            cur.execute('SELECT max(id) from skills')
            id1=cur.fetchone()
            cur.execute('INSERT into skills_cv values (?,?,?)',(id1,max,form.skills[i].level))

    for i in range (1,len(form.hobbies)):
        cur.execute('Select id from hobbies where name=(?) and Job_ID=(?)',(form.hobbies[i].name,),(form.jobID,))
        id=cur.fetchone()
        if id!=None:
            cur.execute('INSERT into hobbies_cv values (?,?,?)',(id,max,form.hobbies[i].level))
        else:
            new_traits(form.jobID,form.hobbies[i].name,hobbies)
            cur.execute('SELECT max(id) from hobbies')
            id1=cur.fetchone()
            cur.execute('INSERT into hobbies_cv values (?,?,?)',(id1,max,form.hobbies[i].level))

    for i in range (1,len(form.languages)):
        cur.execute('Select id from languages where name=(?) and Job_ID=(?)',(form.languages[i].name,),(form.jobID,))
        id=cur.fetchone()
        if id!=None:
            cur.execute('INSERT into languages_cv values (?,?,?)',(id,max,form.languages[i].level))
        else:
            new_traits(form.jobID,form.languages[i].name,languages)
            cur.execute('SELECT max(id) from languages')
            id1=cur.fetchone()
            cur.execute('INSERT into languages_cv values (?,?,?)',(id1,max,form.languages[i].level))

    for i in range (1,len(form.ALevels)):
        cur.execute('Select id from alevel where name=(?) and Job_ID=(?)',(form.ALevels[i].name,),(form.jobID,))
        id=cur.fetchone()
        if id!=None:
            cur.execute('INSERT into alevel_cv values (?,?,?)',(id,max,form.ALevels[i].level))
        else:
            new_traits(form.jobID,form.ALevels[i].name,alevels)
            cur.execute('SELECT max(id) from languages')
            id1=cur.fetchone()
            cur.execute('INSERT into languages_cv values (?,?,?)',(id1,max,form.languages[i].level))

    for i in range (1,len(form.degrees)):
        cur.execute('Select id from degrees where name=(?) and Job_ID=(?) and position=(?)',(form.degrees[i].name,),(form.jobID,),(form.degrees[i].position,))
        id=cur.fetchone()
        if id!=None:
            cur.execute('INSERT into degrees_cv values (?,?,?)',(id,max,form.degrees[i].level))
        else:
            new_degree(form.jobID,form.degrees[i].name,form.degrees[i].position)
            cur.execute('SELECT max(id) from degrees')
            id1=cur.fetchone()
            cur.execute('INSERT into degrees_cv values (?,?,?)',(id1,max,form.degrees[i].level))

    for i in range (1,len(form.employment)):
        cur.execute('Select id from employment where name=(?) and Job_ID=(?) and position=(?)',(form.employment[i].name,),(form.jobID,),(form.employment[i].course,))
        id=cur.fetchone()
        if id!=None:
            cur.execute('INSERT into employment_cv values (?,?,?)',(id,max,form.employment[i].level))
        else:
            new_employment(form.jobID,form.employment[i].name,form.employment[i].course)
            cur.execute('SELECT max(id) from employment')
            id1=cur.fetchone()
            cur.execute('INSERT into employment_cv values (?,?,?)',(id1,max,form.employment[i].level))

    con.commit()
    con.close()

def apply_job(cvID,jobID):
    con = sql.connect(path.join(ROOT, 'test.db'))
    cur = con.cursor()
    cur.execute('INSERT into job_cv values (?,?,?,?)',(jobID,cvID,0,0))
    con.close()
