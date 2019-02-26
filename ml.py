import matlab.engine
import users
import time
import numpy

skills = users.selectAllSkills()
languages = users.selectAllLanguages()
ALevels = users.selectAllAlevels()
hobbies = users.selectAllHobbies()
employment = users.selectAllEmployment()

dict = {'A*' : 10, 'A' : 9, 'B' : 8, 'C' : 7, 'D' : 6}
g_numOfCVs = 100
g_numOfTestCVs = 100

trainingData = []
testData = []
state = []
state2 = []

jobID = 1 #Which job it is

def getData(databaseData, globalData, dataSet, index = 0, resultSet = []):
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

    if index == 2:
        if applicant_level.get('Chinese') != None:
            resultSet.append(1)
        else:
            resultSet.append(0)

for i in range(1, g_numOfCVs + 1):
    info = users.get_CV(i)
    getData(info.skills, skills, trainingData, 2, state)
    getData(info.languages, languages, trainingData)
    getData(info.ALevels, ALevels, trainingData, 1)
    getData(info.hobbies, hobbies, trainingData)

    '''
    applicant_data = []
    applicant_level = {}
    for item in info.employment:
        applicant_data.append(item.name)
        applicant_level[item.name] = item.length
    for item in employment:
        if item not in applicant_data:
            trainingData.append(0)
        else:
            trainingData.append(applicant_level[item])
    '''

for i in range(1, g_numOfTestCVs + 1):
    info = users.get_CV(i)

    getData(info.skills, skills, testData, 2, state2)
    getData(info.languages, languages, testData)
    getData(info.ALevels, ALevels, testData, 1)
    getData(info.hobbies, hobbies, testData)


X1 = numpy.array(trainingData)
X2 = numpy.array(testData)
y1 = numpy.array(state)
y2 = numpy.array(state2)


eng = matlab.engine.start_matlab()
t = eng.main(X1.tolist(), y1.tolist(), g_numOfCVs, X2.tolist(), y2.tolist())
for i in range(0, 101):
    users.update_status(1, i + 1, 1)

for i in range(1, 101):
    users.select_status(1, i)
