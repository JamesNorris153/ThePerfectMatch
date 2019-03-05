#In python version of machine learning, we will run our process based on sklearn
#Using this prebuild library, we do not need to do all the maths by ourselves
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.externals import joblib

def doLearning(X1, y1, X2):
    #This function is used to get the output layer of the neural network
    #which will be the exact predicted scores of the CVs instead of their rounded
    #value as 0 and 1.
    def get_activations(clf, X):
        hidden_layer_sizes = clf.hidden_layer_sizes
        if not hasattr(hidden_layer_sizes, "__iter__"):
            hidden_layer_sizes = [hidden_layer_sizes]
        hidden_layer_sizes = list(hidden_layer_sizes)
        layer_units = [X.shape[1]] + hidden_layer_sizes + \
            [clf.n_outputs_]
        activations = [X]
        for i in range(clf.n_layers_ - 1):
            activations.append(np.empty((X.shape[0],
                                         layer_units[i + 1])))
        clf._forward_pass(activations)
        return activations[-1]

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
    #return the predicted scores 
    return get_activations(mlp, X2)
