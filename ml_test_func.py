import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.externals import joblib

def ml_test(X1, y1, X2, y2):
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
    X1 = scaler.transform(X1)
    X2 = scaler.transform(X2)
    mlp = MLPClassifier(hidden_layer_sizes=(12,12), max_iter=10000)
    mlp.fit(X1, y1)
    predictions = mlp.predict(X2)
    print(mlp.score(X2, y2))
