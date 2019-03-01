import matlab.engine
import users
import time
import numpy

def retrain(jobID):
    cvs = users.select_cvs(jobID)
    skills = users.selectAllSkills()
    languages = users.selectAllLanguages()
    ALevels = users.selectAllAlevels()
    hobbies = users.selectAllHobbies()
    employment = users.selectAllEmployment()

    dict = {'A*' : 10, 'A' : 9, 'B' : 8, 'C' : 7, 'D' : 6}

    trainingData = []
    testData = []
    state = []

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
        if users.select_status(jobID, i)[0] == 0:
            getData(info.skills, skills, testData, 2)
            getData(info.languages, languages, testData)
            getData(info.ALevels, ALevels, testData, 1)
            getData(info.hobbies, hobbies, testData)
        else:
            getData(info.skills, skills, trainingData, 2)
            getData(info.languages, languages, trainingData)
            getData(info.ALevels, ALevels, trainingData, 1)
            getData(info.hobbies, hobbies, trainingData)
            status.append(users.select_status(jobID, i)[0])

    X1 = numpy.array(trainingData)
    X2 = numpy.array(testData)
    y1 = numpy.array(state)

    eng = matlab.engine.start_matlab()
    eng.addpath(r'./functions',nargout=0)
    t = eng.main(X1.tolist(), y1.tolist(), len(cvs), X2.tolist())
    for i in cvs:
        users.update_score(jobID, i, t[0])
