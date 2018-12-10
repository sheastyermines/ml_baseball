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


conn = sqlite3.connect('lahman2016.sqlite')

# Querying Database for all seasons where a team played 150 or more games and is still active today. 
query = '''select * from Teams 
inner join TeamsFranchises
on Teams.franchID == TeamsFranchises.franchID
where Teams.G >= 150 and TeamsFranchises.active == 'Y';
'''

# Convert results to DataFrame
allData = pd.read_sql_query(query, conn)

#prune unncesisary columns
prunedData = allData[["yearID","franchID","divID","Rank","G",
                "Ghome","W","L","DivWin","WCWin","LgWin","WSWin", "R", "AB",
                "H", "2B", "3B", "HR", "BB", "SO", "SB", "CS", 
                "RA", "ER", "ERA", "CG", "SHO", "SV", "IPouts", "HA", "HRA",
                "BBA", "SOA", "E", "DP", "FP", "attendance", "BPF", "PPF"]]

exampleData = allData[["Rank","G",
                "Ghome", "W", "L", "R", "AB",
                "H", "2B", "3B", "HR", "BB", "SO", "SB", "CS",
                "RA", "ER", "ERA", "CG", "SHO", "SV", "IPouts", "HA", "HRA",
                "BBA", "SOA", "E", "DP", "FP", "attendance", "BPF", "PPF"]]

#drop columns with bad data
exampleData = exampleData.dropna()

exampleData = exampleData.astype(float)

#get wins from data and remove W/L/G from the vectors
exampleWins = exampleData["W"]
exampleData = exampleData[["Rank","G",
                "Ghome", "R", "AB",
                "H", "2B", "3B", "HR", "BB", "SO", "SB", "CS",
                "RA", "ER", "ERA", "CG", "SHO", "SV", "IPouts", "HA", "HRA",
                "BBA", "SOA", "E", "DP", "FP", "attendance", "BPF", "PPF"]]


print(exampleData)

#get the training and testing data
X_train, X_test, y_train, y_test = train_test_split(exampleData, exampleWins, random_state=0, test_size=0.2)

print(X_train.shape)
print(y_train.shape)

#reshape the data to use the scalers
y_train = y_train.values.reshape((-1,1))
y_test = y_test.values.reshape((-1,1))
print(y_train.shape)

#fit the data to the scalers
scalerY = preprocessing.StandardScaler();
scalerY.fit(y_train)
scalerX = preprocessing.StandardScaler();
scalerX.fit(X_train)

#transform the data based on the scalers
X_train = scalerX.transform(X_train)
y_train = scalerY.transform(y_train)
X_test = scalerX.transform(X_test)
y_test = scalerY.transform(y_test)

#define the network
layers = [
    Dense(100, input_shape=(exampleData.shape[1],)),
    Dense(100),
    Dense(100),
    Dense(1)
]

model = Sequential(layers);

#train the network
model.compile(optimizer="SGD", loss='mean_squared_error', metrics=['mean_absolute_error'])
model.fit(X_train, y_train, epochs=1000, verbose=0)
print(model.evaluate(x=X_test, y=y_test))


#print(model.predict(X_train[0:8]))
print(scalerY.inverse_transform(y_test[0:8]))
print(scalerY.inverse_transform(model.predict(X_test[0:8])))

#residuals for debuging
a = scalerY.inverse_transform(model.predict(X_test)) - scalerY.inverse_transform(y_test)
a = a.astype(int)

#preditct
predictions = scalerY.inverse_transform(model.predict(X_test))

#get the properly scaled metrics
print(metrics.mean_squared_error(scalerY.inverse_transform(y_test),predictions))
print(metrics.mean_absolute_error(scalerY.inverse_transform(y_test),predictions))

#save the models and transformers
model.save('singleModel.h5')
scaler_filename = "singleModelYscaler.save"
joblib.dump(scalerY, scaler_filename)
scaler_filename = "singleModelXscaler.save"
joblib.dump(scalerX, scaler_filename)
