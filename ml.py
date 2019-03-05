import users
import time
import numpy as np
import ml_func
import re

#retrain the whole CVs with jobID to predict the new CVs' score
#training data - cvs with status 1 or 2(has been liked/disliked)
#test data - cvs with status 0(has noe been made a choice)
def retrain(jobID):
    #select all the cvs with a jobID
    cvs = users.select_cvs_completed(jobID)
    #select all the existing skills
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
    X2 = []
    #y1 is used to store the y(status) value of training data
    #y1 is a 2D array, which every row represents the status of one cv
    y1 = []
    #newApplicants is used to store the cvID of CVs with status as 0
    #In order to update their score after machine learning
    newApplicants = []

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

    #go through all the cvs we selected with jobID and get the data we need in X1, X2, y1.
    for i in cvs:
        #info will be the whole data information of this cv
        info = users.get_CV(i[0])
        #status is whether current cv has been made a choice on
        status = users.select_status(jobID, i[0])[0]
        #applicant is an array used to store all of the feature values of the current applicant
        #we will push this array in X1 or X2 in the end.
        applicant = []
        #get the university name of the cv and convert it into numbers by convertUniScore()
        applicant.append(convertUniScore(info.degrees[0].name))
        #get the degree value of the cv
        applicant.append(degree[info.degrees[0].grade])
        #get the test score of the cv
        applicant.append(users.select_testScore(jobID, i[0])[0])
        #check status value
        #1/2 - training data
        #0 - test data
        if status == 0:
            #if it is test data then we put the cvID of this cv into newApplicants
            newApplicants.append(i[0])
            getData(info.skills, skills, applicant, 2)
            getData(info.languages, languages, applicant)
            getData(info.ALevels, ALevels, applicant, 1)
            getData(info.hobbies, hobbies, applicant)
            X2.append(applicant)
        else:
            getData(info.skills, skills, applicant, 2)
            getData(info.languages, languages, applicant)
            getData(info.ALevels, ALevels, applicant, 1)
            getData(info.hobbies, hobbies, applicant)
            X1.append(applicant)
            level = []
            #convert status values to 1 - like 0 - dislike
            if status == 1: level.append(1)
            else: level.append(0)
            y1.append(level)

    #call machine learning function to do the training and prediction
    newScore = ml_func.doLearning(X1, y1, X2)

    #after we get the predicted score for each cv, we update every new cv with its score
    index = 0
    for i in newApplicants:
        users.update_score(jobID, i, newScore[index][0])
        index = index + 1
