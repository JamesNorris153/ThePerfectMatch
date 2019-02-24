import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
from users import Applicant, create_user, insert_json_cv, Form, Edu, Emp
import bcrypt

def read():
    id=1
    with open('data.json') as f:
        data = json.load(f)
    for i in data:
        temp = Applicant(i['Name'].split()[0],i['Name'].split()[1],"a",str(id))
        create_user(temp)
        insert_json_cv(i,id)
        id+=1

read()
