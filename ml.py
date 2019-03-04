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
        status = users.select_status(jobID, i[0])[0]
        if status == 0:
            newApplicants.append(i[0])
            applicant = []
            getData(info.skills, skills, applicant, 2)
            getData(info.languages, languages, applicant)
            getData(info.ALevels, ALevels, applicant, 1)
            getData(info.hobbies, hobbies, applicant)
            X2.append(applicant)
        else:
            applicant = []
            level = []
            getData(info.skills, skills, applicant, 2)
            getData(info.languages, languages, applicant)
            getData(info.ALevels, ALevels, applicant, 1)
            getData(info.hobbies, hobbies, applicant)
            X1.append(applicant)
            if status == 1: level.append(1)
            else: level.append(0)
            y1.append(level)

    newScore = ml_func.doLearning(X1, y1, X2)

    index = 0
    for i in newApplicants:
        print(jobID)
        print(i)
        print(newScore[index][0])
        users.update_score(jobID, i, newScore[index][0])
        index = index + 1

# retrain(1)
