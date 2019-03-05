import users
import time
import numpy as np
import ml_test_func
import re

#numOfTrainingData - how many training CVs to select
#numOfTestData - how many test CVs to test
#This function will show how accurate our machine learning program is
#by comparing the status of test data with the predicted status after our
#machine learning program
def test(jobID, numOfTrainingData, numOfTestData):
    cvs = users.select_cvs_completed(jobID)
    #If
    if numOfTestData + numOfTrainingData > len(cvs): return
    #select all the cvs with a jobID
    skills = users.selectAllSkills()
    #select all the existing languages
    languages = users.selectAllLanguages()
    #select all the existing A-levels
    ALevels = users.selectAllAlevels()
    #select all the existing hobbies
    hobbies = users.selectAllHobbies()

    #map A-levels grades to numbers
    dict = {'A*' : 10, 'A' : 9, 'B' : 8, 'C' : 7, 'D' : 6, 'E' : 5, 'F' : 4, 'G' : 3, 'U' : 2}

    #map university degrees to numbers
    degree = {'1st' : 10, '2:1' : 9, '2:2' : 8, '3rd' : 7, 'Pass' : 6}

    #X1 is used to store the features of training data
    #X1 is a 2D array, which every row represents the feature values of one cv
    X1 = []
    #X2 is used to store the features of test data
    #X2 is a 2D array, which every row represents the feature values of one cv
    X2 = []#
    #y1 is used to store the y(status) value of training data
    #y1 is a 2D array, which every row represents the status of one cv
    y1 = []
    #y2 is used to store the y(status) value of test data
    #y2 is a 2D array, which every row represents the status of one cv
    y2 = []

    #read university score from QSranking and store them as a map from string to double in uniScore
    uniScore = {}
    def readUniScore():
        with open("uniScore.txt") as f:
            for line in f:
                m = re.search("\d", line)
                if m :
                    uniScore[line[:m.start() - 1]] = line[m.start():]

    readUniScore()

    #find the university scoreself.
    #return 0 if the university not found
    def convertUniScore(uniName):
        if uniScore.get(uniName.upper()) != None:
            return uniScore[uniName.upper()]
        else:
            return 0

    #get feature values for training data and test data
    #databaseData - section of cv data select from database, skills, languages, ALevels, etc.
    #globalData - the set of all existing section of cv which has been selected before
    #dataSet - where to put the select data into
    def getData(databaseData, globalData, dataSet, index = 0):
        #applicant_data is used to store the name of current CV's existing data
        applicant_data = []
        #applicant_level is used to store the level of current CV's existing data
        #reason to use these two containers is databaseData pass an array of objects to this function,
        #we cannot directly select what we want from an object
        applicant_level = {}
        #record applicant's name and level of data
        for item in databaseData:
            applicant_data.append(item.name)
            applicant_level[item.name] = item.level
        #go through the existing array of current section, if current applicant does not have one skill,
        #then the feature value of that skill will be 0, otherwise it will be the applicant's level.
        for item in globalData:
            if item not in applicant_data:
                dataSet.append(0)
            else:
                if index == 1: dataSet.append(dict[applicant_level[item]])
                else: dataSet.append(applicant_level[item])

    #go through the numOfTrainingData of CVs and store their features and status in X1 and y1
    for i in range(0, numOfTrainingData + numOfTestData):
        #applicant is an array used to store all of the feature values of the current applicant
        #we will push this array in X1 or X2 in the end.
        applicant = []
        level = []
        #info will be the whole data information of this cv
        info = users.get_CV(cvs[i][0])
        #get the university name of the cv and convert it into numbers by convertUniScore()
        applicant.append(convertUniScore(info.degrees[0].name))
        #get the degree value of the cv
        applicant.append(degree[info.degrees[1].grade])
        #get the test score of the cv
        applicant.append(users.select_testScore(jobID, i[0])[0])
        getData(info.skills, skills, applicant, 2)
        getData(info.languages, languages, applicant)
        getData(info.ALevels, ALevels, applicant, 1)
        getData(info.hobbies, hobbies, applicant)
        #status is whether current cv has been made a choice on
        status = users.select_status(jobID, cvs[i][0])[0]
        #convert status values to 1 - like 0 - dislike
        if status == 1: level.append(1)
        else: level.append(0)
        if i < numOfTrainingData:
            X1.append(applicant)
            y1.append(level)
        else:
            X2.append(applicant)
            y2.append(level)

    #Call ml_test() to get the accuracy of our program
    ml_test_func.ml_test(X1, y1, X2, y2)
