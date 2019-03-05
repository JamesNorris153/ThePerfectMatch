#In python version of machine learning, we will run our process based on sklearn
#Using this prebuild library, we do not need to do all the maths by ourselves
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.externals import joblib

def ml_test(X1, y1, X2, y2):
    scaler = StandardScaler()
    scaler.fit(X1)
    #scaler.transform() is used to transform data from wide range to numbers close
    #to 0 to make our later calculation a lot quicker
    X1 = scaler.transform(X1)
    X2 = scaler.transform(X2)
    #set the number of hidden layers as 12 and number of iterations as 10000
    mlp = MLPClassifier(hidden_layer_sizes=(12,12), max_iter=10000)
    #run the machine learning training on X1 and y1
    mlp.fit(X1, y1)
    #get prediction values of X2
    predictions = mlp.predict(X2)
    #compare the value of X2 and y2 to get our accuracy
    print(mlp.score(X2, y2))
