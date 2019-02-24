from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    FName = db.Column(db.String(30), unique=False, nullable=False)
    LName = db.Column(db.String(30), unique=False, nullable=False)
    password = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    cvs=db.relationship('CVs',backref='user',lazy=True)

    def __repr__(self):
        return f"User('{self.FName}', '{self.LName}', '{self.email}')"

class Admins(db.Model):
    __tablename__='admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=False, nullable=False)
    password = db.Column(db.String(30), unique=False, nullable=False)

    def __repr__(self):
        return f"Users('{self.id}', '{self.username}')"

class Jobs(db.Model):
    __tablename__='jobs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)
    deadline = db.Column(db.DateTime, unique=False, nullable=False)
    location = db.Column(db.String(50), unique=False, nullable=False)
    position = db.Column(db.String(20), unique=False, nullable=False)
    alevels=db.relationship('ALevel',backref='job',lazy=True)
    skills=db.relationship('Skills',backref='job',lazy=True)
    employment=db.relationship('Employment',backref='job',lazy=True)
    langages=db.relationship('Languages',backref='job',lazy=True)
    hobbies=db.relationship('Hobbies',backref='job',lazy=True)
    degrees=db.relationship('Degrees',backref='job',lazy=True)
    tests=db.relationship('Tests',backref='job',lazy=True)

    def __repr__(self):
        return f"Jobs('{self.name}', '{self.description}', '{self.deadline}', '{self.location}', '{self.position}')"

class ALevel(db.Model):
    __tablename__='alevel'
    id = db.Column(db.Integer, primary_key=True)
    Job_ID= db.Column(db.Integer,db.ForeignKey('jobs.id'), nullable=False)
    name = db.Column(db.String(30), unique=False, nullable=False)
    level = db.Column(db.Integer, unique=False, default=0)
    b=db.relationship('CVs',secondary="alevel_cv")

    def __repr__(self):
        return f"ALevel('{self.subject}')"

class Skills(db.Model):
    __tablename__='skills'
    id = db.Column(db.Integer, primary_key=True)
    Job_ID= db.Column(db.Integer,db.ForeignKey('jobs.id'), nullable=False)
    name = db.Column(db.String(30), unique=False, nullable=False)
    level = db.Column(db.Integer, unique=False, default=0)
    b=db.relationship('CVs',secondary="skills_cv")

    def __repr__(self):
        return f"Skills('{self.skill}')"

class Employment(db.Model):
    __tablename__="employment"
    id = db.Column(db.Integer, primary_key=True)
    Job_ID= db.Column(db.Integer,db.ForeignKey('jobs.id'), nullable=False)
    company = db.Column(db.String(30), unique=False, nullable=False)
    position = db.Column(db.String(30), unique=False, nullable=False)
    level = db.Column(db.Integer, unique=False, default=0)
    b=db.relationship('CVs',secondary="employment_cv")

    def __repr__(self):
        return f"Employment('{self.company}','{self.position}')"

class CVs(db.Model):
    __tablename__='cvs'
    id = db.Column(db.Integer, primary_key=True)
    User_ID= db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    a=db.relationship('ALevel',secondary="alevel_cv")

    def __repr__(self):
        return f"CVs('{self.id}', '{self.User_ID}')"

class Languages(db.Model):
    __tablename__="languages"
    id = db.Column(db.Integer, primary_key=True)
    Job_ID= db.Column(db.Integer,db.ForeignKey('jobs.id'), nullable=False)
    name = db.Column(db.String(30), unique=False, nullable=False)
    level = db.Column(db.Integer, unique=False, default=0)
    b=db.relationship('CVs',secondary="language_cv")

    def __repr__(self):
        return f"Languages('{self.language}')"

class Hobbies(db.Model):
    __tablename__="hobbies"
    id = db.Column(db.Integer, primary_key=True)
    Job_ID= db.Column(db.Integer,db.ForeignKey('jobs.id'), nullable=False)
    name = db.Column(db.String(30), unique=False, nullable=False)
    level = db.Column(db.Integer, unique=False, default=0)
    b=db.relationship('CVs',secondary="hobby_cv")

    def __repr__(self):
        return f"Hobbies('{self.hobby}')"

class Degrees(db.Model):
    __tablename__="degrees"
    id = db.Column(db.Integer, primary_key=True)
    Job_ID= db.Column(db.Integer,db.ForeignKey('jobs.id'), nullable=False)
    university = db.Column(db.String(30), unique=False, nullable=False)
    course = db.Column(db.String(30), unique=False, nullable=False)
    level = db.Column(db.Integer, unique=False, default=0)
    b=db.relationship('CVs',secondary="degree_cv")

    def __repr__(self):
        return f"Degees('{self.university}','{self.course}')"

class Tests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Job_ID= db.Column(db.Integer,db.ForeignKey('jobs.id'), nullable=False)
    questions=db.relationship('Question_Test',backref='test',lazy=True)

class ALevel_CV(db.Model):
    __tablename__ = 'alevel_cv'
    CV_ID= db.Column(db.Integer, db.ForeignKey('cvs.id'), primary_key=True)
    ALevel_ID = db.Column(db.Integer, db.ForeignKey('alevel.id'), primary_key=True)
    grade = db.Column(db.String(10), unique=False, nullable=False)
    aa = relationship(ALevel,backref=backref("alevel_cv", cascade="all, delete-orphan"))
    cc = relationship(CVs, backref=backref("alevel_cv", cascade="all, delete-orphan"))

class Skills_CV(db.Model):
    __tablename__ = 'skills_cv'
    Skills_ID = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False, primary_key=True)
    CV_ID= db.Column(db.Integer, db.ForeignKey('cvs.id'), nullable=False, primary_key=True)
    expertise = db.Column(db.Integer, unique=False, nullable=False)
    ss = relationship(Skills,backref=backref("skills_cv", cascade="all, delete-orphan"))
    cc = relationship(CVs, backref=backref("skills_cv", cascade="all, delete-orphan"))

class Employment_CV(db.Model):
    __tablename__ = 'employment_cv'
    Employment_ID = db.Column(db.Integer, db.ForeignKey('employment.id'), nullable=False, primary_key=True)
    CV_ID= db.Column(db.Integer, db.ForeignKey('cvs.id'), nullable=False, primary_key=True)
    length = db.Column(db.String(20), unique=False, nullable=False)
    ss = relationship(Employment,backref=backref("employment_cv", cascade="all, delete-orphan"))
    cc = relationship(CVs, backref=backref("employment_cv", cascade="all, delete-orphan"))

class Language_CV(db.Model):
    __tablename__ = 'language_cv'
    Language_ID = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False, primary_key=True)
    CV_ID= db.Column(db.Integer, db.ForeignKey('cvs.id'), nullable=False, primary_key=True)
    expertise = db.Column(db.Integer, unique=False, nullable=False)
    ss = relationship(Languages,backref=backref("language_cv", cascade="all, delete-orphan"))
    cc = relationship(CVs, backref=backref("language_cv", cascade="all, delete-orphan"))

class Hobby_CV(db.Model):
    __tablename__ = 'hobby_cv'
    Hobby_ID = db.Column(db.Integer, db.ForeignKey('hobbies.id'), nullable=False, primary_key=True)
    CV_ID= db.Column(db.Integer, db.ForeignKey('cvs.id'), nullable=False, primary_key=True)
    interest = db.Column(db.Integer, unique=False, nullable=False)
    ss = relationship(Hobbies,backref=backref("hobby_cv", cascade="all, delete-orphan"))
    cc = relationship(CVs, backref=backref("hobby_cv", cascade="all, delete-orphan"))

class Job_CV(db.Model):
    __tablename__ = 'job_cv'
    Job_ID = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False, primary_key=True)
    CV_ID= db.Column(db.Integer, db.ForeignKey('cvs.id'), nullable=False, primary_key=True)
    score = db.Column(db.Integer, unique=False, nullable=False)
    status = db.Column(db.Integer, unique=False, nullable=False)
    ss = relationship(Jobs,backref=backref("job_cv", cascade="all, delete-orphan"))
    cc = relationship(CVs, backref=backref("job_cv", cascade="all, delete-orphan"))

class Degree_CV(db.Model):
    __tablename__ = 'degree_cv'
    Degree_ID = db.Column(db.Integer, db.ForeignKey('degrees.id'), nullable=False, primary_key=True)
    CV_ID= db.Column(db.Integer, db.ForeignKey('cvs.id'), nullable=False, primary_key=True)
    grade = db.Column(db.String(30), unique=False, nullable=False)
    dd = relationship(Degrees,backref=backref("degree_cv", cascade="all, delete-orphan"))
    cc = relationship(CVs, backref=backref("degree_cv", cascade="all, delete-orphan"))

class Question_Test(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Test_ID= db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    question = db.Column(db.Text, unique=False, nullable=False)
    answer = db.Column(db.Text, unique=False, nullable=False)

    def __repr__(self):
        return f"Question_Test('{self.question}','{self.answer}')"
