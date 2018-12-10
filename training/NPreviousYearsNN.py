#This file generates the .a5 file for the N previous years model

import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from sklearn import *
import numpy as np
import scipy
import matplotlib
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib

#change the files based on the value of N
exampleData = pd.read_pickle('1YearsX.pkl')
exampleWins = pd.read_pickle('1YearsY.pkl')

print(exampleData.shape)

#exampleData = exampleData[0:476]
#exampleWins = exampleWins[0:476]

X_train, X_test, y_train, y_test = train_test_split(exampleData, exampleWins, random_state=0, test_size=0.2)

print(X_train.shape)
print(y_train.shape)

#reshape to fit standard scaler expected output
y_train = y_train.values.reshape((-1,1))
y_test = y_test.values.reshape((-1,1))

#fit scalers
scalerY = preprocessing.StandardScaler();
scalerY.fit(y_train)
scalerX = preprocessing.StandardScaler();
scalerX.fit(X_train)

#transform data
X_train = scalerX.transform(X_train)
y_train = scalerY.transform(y_train)
X_test = scalerX.transform(X_test)
y_test = scalerY.transform(y_test)

#neural network training definition
layers = [
    Dense(100, input_shape=(exampleData.shape[1],)),
    Dropout(0.1),
    Dense(100, activation = 'relu'),
    Dropout(0.1),
    Dense(100, activation = 'relu'),
    Dropout(0.1),
    Dense(100, activation = 'relu'),
    Dropout(0.1),
    Dense(1)
]

model = Sequential(layers);

#train the model
model.compile(optimizer="SGD", loss='mean_squared_error', metrics=['mean_absolute_error'])
model.fit(X_train, y_train, epochs=1000, verbose=0)

#evaluate the model (still scalled wierdly)
#print(model.evaluate(x=X_train, y=y_train, verbose=0)) #to check for overfitting
print(model.evaluate(x=X_test, y=y_test, verbose=0)) #acutal score

#print 8 potential squares
print(scalerY.inverse_transform(y_test[0:8]))
print(scalerY.inverse_transform(model.predict(X_test[0:8])))

#residual array for debuging purposes
a = scalerY.inverse_transform(model.predict(X_test)) - scalerY.inverse_transform(y_test)
a = a.astype(int)

#predicted values
predictions = scalerY.inverse_transform(model.predict(X_test))

#get statistics
print(metrics.mean_squared_error(scalerY.inverse_transform(y_test),predictions))
print(metrics.mean_absolute_error(scalerY.inverse_transform(y_test),predictions))

#save the model and the scalers (change name for other numbers of years)
model.save('1yearModel.h5')
scaler_filename = "1yearModelYscaler.save"
joblib.dump(scalerY, scaler_filename)
scaler_filename = "1yearModelXscaler.save"
joblib.dump(scalerX, scaler_filename) 
