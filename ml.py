import users
import time
import numpy as np
import ml_func
import re

def retrain(jobID):
    # cvs = users.select_cvs(jobID)
    cvs = users.select_cvs_completed(jobID)
    skills = users.selectAllSkills()
    languages = users.selectAllLanguages()
    ALevels = users.selectAllAlevels()
    hobbies = users.selectAllHobbies()
    employment = users.selectAllEmployment()
    # skills = users.selectAllSkills(jobID)
    # languages = users.selectAllLanguages(jobID)
    # ALevels = users.selectAllAlevels(jobID)
    # hobbies = users.selectAllHobbies(jobID)
    # employment = users.selectAllEmployment(jobID)

    uniScore = {}
    def readUniScore():
        with open("uniScore.txt") as f:
            for line in f:
                m = re.search("\d", line)
                if m :
                    uniScore[line[:m.start() - 1]] = line[m.start():]

    readUniScore()

    def convertUniScore(uniName):
        if uniScore.get(uniName) != None:
            return uniScore[uniName]
        else:
            return 0

    dict = {'A*' : 10, 'A' : 9, 'B' : 8, 'C' : 7, 'D' : 6}
    degree = {'1st' : 10, '2:1' : 9, '2:2' : 8, '3rd' : 7, 'Pass' : 6}
    X1 = []
    X2 = []
    y1 = []
    y2 = []
    newApplicants = []

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
        applicant = []
        print(info.degrees[0])
        applicant.append(convertUniScore(info.degrees[0].name))
        applicant.append(degree[info.degrees[0].grade])
        applicant.append(users.select_testScore(jobID, i[0]))
        if status == 0:
            newApplicants.append(i[0])
            getData(info.skills, skills, applicant, 2)
            getData(info.languages, languages, applicant)
            getData(info.ALevels, ALevels, applicant, 1)
            getData(info.hobbies, hobbies, applicant)
            X2.append(applicant)
        else:
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
        users.update_score(jobID, i, newScore[index][0])
        index = index + 1
