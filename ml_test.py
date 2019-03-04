import users
import time
import numpy as np
import ml_test_func

def test(jobID, numOfTrainingData, numOfTestData):
    cvs = users.select_cvs(jobID)
    if numOfTestData + numOfTrainingData > len(cvs): return
    skills = users.selectAllSkills()
    languages = users.selectAllLanguages()
    ALevels = users.selectAllAlevels()
    hobbies = users.selectAllHobbies()
    employment = users.selectAllEmployment()

    dict = {'A*' : 10, 'A' : 9, 'B' : 8, 'C' : 7, 'D' : 6}

    X1 = []
    X2 = []
    y1 = []
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

    for i in range(0, numOfTrainingData):
        applicant = []
        level = []
        info = users.get_CV(cvs[i][0])
        getData(info.skills, skills, applicant, 2)
        getData(info.languages, languages, applicant)
        getData(info.ALevels, ALevels, applicant, 1)
        getData(info.hobbies, hobbies, applicant)
        applicant.append(users.select_testScore(jobID, cvs[i][0]))
        X1.append(applicant)
        status = users.select_status(jobID, cvs[i][0])[0]
        if status == 1: level.append(1)
        else: level.append(0)
        y1.append(level)

    for i in range(numOfTrainingData, numOfTestData + numOfTrainingData):
        info = users.get_CV(cvs[i][0])
        applicant = []
        level = []
        getData(info.skills, skills, applicant, 2)
        getData(info.languages, languages, applicant)
        getData(info.ALevels, ALevels, applicant, 1)
        getData(info.hobbies, hobbies, applicant)
        applicant.append(users.select_testScore(jobID, cvs[i][0]))
        X2.append(applicant)
        status = users.select_status(jobID, cvs[i][0])[0]
        if status == 1: level.append(1)
        else: level.append(0)
        y2.append(level)

    ml_test_func.ml_test(X1, y1, X2, y2)
