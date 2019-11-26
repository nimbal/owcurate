import pandas as pd
import numpy as np
import sklearn
from sklearn.neighbors import KNeighborsClassifier
import tensorflow as tf
import keras
from keras.models import Sequential
from keras import layers
from sklearn import preprocessing, linear_model

data = pd.read_csv("DATA.csv")
data = data.drop(["Unnamed: 0"], axis=1)

X = data.drop(["300"], axis=1)
y = data["300"]

X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2)

model = KNeighborsClassifier(n_neighbors=7)

model.fit(X_train, y_train)

acc = model.score(X_test, y_test)

print(acc)













