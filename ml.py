import matlab.engine
import users
import time
import numpy as np
import ml_func

def retrain(jobID):
    cvs = users.select_cvs(jobID)
    skills = users.selectAllSkills()
    languages = users.selectAllLanguages()
    ALevels = users.selectAllAlevels()
    hobbies = users.selectAllHobbies()
    employment = users.selectAllEmployment()

    dict = {'A*' : 10, 'A' : 9, 'B' : 8, 'C' : 7, 'D' : 6}

    X1 = []
    X2 = []
    y1 = []
    newApplicants = []
    y2 = []
    def getData(databaseData, globalData, dataSet, index = 0):
        applicant_data = []
        applicant_level = {}
        for item in databaseData:
            applicant_data.append(item.name)
            applicant_level[item.name] = item.level
        for item in globalData:
            if item not in applicant_data:
                dataSet.append(0)
            else:
                if index == 1: dataSet.append(dict[applicant_level[item]])
                else: dataSet.append(applicant_level[item])

    for i in cvs:
        info = users.get_CV(i[0])
        status = users.select_status(jobID, i)[0]
        if status == 0:
            newApplicants.append(i[0])
            getData(info.skills, skills, X2, 2)
            getData(info.languages, languages, X2)
            getData(info.ALevels, ALevels, X2, 1)
            getData(info.hobbies, hobbies, X2)
        else:
            getData(info.skills, skills, X1, 2)
            getData(info.languages, languages, X1)
            getData(info.ALevels, ALevels, X1, 1)
            getData(info.hobbies, hobbies, X1)
            y1.append(status)

    newScore = ml_func.doLearning(X1, y1, X2)

    index = 0
    for i in newApplicants:
        users.update_score(jobID, i, newScore[index])
        index = index + 1

retrain(1)
