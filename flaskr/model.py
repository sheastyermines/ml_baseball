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
from keras.models import load_model

'''
Checks whether or not we have data for a specific year and team name 
df = dataframe to check
team = team name
year = year that you want wins for

returns row index or -1 if row does not exist
'''


def existsInData( df, team, year):
    #checks if a row with the correct team and year exists in the given datafram
    #returns the index of the row (or -1 if no row is found)
    for index, row in df.iterrows():
        if row["franchID"].iloc[0] == team and row["yearID"] == year:
            return index
    return -1

'''
Gets a feature vector for a specific year and team name for the specified model
team = team name
year = year that you want wins for
model = one of the folowing (5years = 5, 3years = 3, 1year = 1, sameYear = 0)

returns row index or -1 if we dont have data for that year
'''

def getFeatureVector(team, year, model):
    conn = sqlite3.connect('flaskr/saved_models/lahman2016.sqlite')

    # Querying Database for all seasons where a team played 150 or more games and is still active today. 
    query = '''select * from Teams 
    inner join TeamsFranchises
    on Teams.franchID == TeamsFranchises.franchID
    where Teams.G >= 150 and TeamsFranchises.active == 'Y';
    '''

    # Convert results to DataFrame
    allData = pd.read_sql_query(query, conn)

    #prunes data that is not usefull
    prunedData = allData[["yearID","franchID","divID","Rank","G",
                    "Ghome","W","L","DivWin","WCWin","LgWin","WSWin", "R", "AB",
                    "H", "2B", "3B", "HR", "BB", "SO", "SB", "CS", 
                    "RA", "ER", "ERA", "CG", "SHO", "SV", "IPouts", "HA", "HRA",
                    "BBA", "SOA", "E", "DP", "FP", "attendance", "BPF", "PPF"]]

    prunedData = prunedData.dropna()

    #print(prunedData)

    #get the data that will be in feature vectors
    exampleData = prunedData[["Rank","G",
                    "Ghome", "W", "L", "R", "AB",
                    "H", "2B", "3B", "HR", "BB", "SO", "SB", "CS",
                    "RA", "ER", "ERA", "CG", "SHO", "SV", "IPouts", "HA", "HRA",
                    "BBA", "SOA", "E", "DP", "FP", "attendance", "BPF", "PPF"]]

    #exampleData = exampleData.dropna()

    exampleData = exampleData.astype(float)

    '''
    exampleWins = exampleData["W"]
    exampleData = exampleData[["Rank","G",
                    "Ghome", "R", "AB",
                    "H", "2B", "3B", "HR", "BB", "SO", "SB", "CS",
                    "RA", "ER", "ERA", "CG", "SHO", "SV", "IPouts", "HA", "HRA",
                    "BBA", "SOA", "E", "DP", "FP", "attendance", "BPF", "PPF"]]
    '''
    if model == 5:
        year1 = existsInData( prunedData, team, year - 1)
        year2 = existsInData( prunedData, team, year - 2)
        year3 = existsInData( prunedData, team, year - 3)
        year4 = existsInData( prunedData, team, year - 4)
        year5 = existsInData( prunedData, team, year - 5)
        if year1 != -1 and year2 != -1 and year3 != -1 and year4 != -1 and year5 != -1:
            #get all 5 previous years
            first = exampleData.loc[[year1]]
            second = exampleData.loc[[year2]]
            third = exampleData.loc[[year3]]
            fourth = exampleData.loc[[year4]]
            fifth = exampleData.loc[[year5]]
            #reset indexes on previous years
            first.reset_index(drop=True,inplace=True)
            second.reset_index(drop=True,inplace=True)
            third.reset_index(drop=True,inplace=True)
            fourth.reset_index(drop=True,inplace=True)
            fifth.reset_index(drop=True,inplace=True)

            '''
            print(prunedData.loc[[year1]])
            print(first)
            print(prunedData.loc[[year2]])
            print(second)
            print(prunedData.loc[[year3]])
            print(third)
            print(prunedData.loc[[year4]])
            print(fourth)
            print(prunedData.loc[[year5]])
            print(fifth)
            '''
            
            #concatinate all previous years
            final = pd.concat([first,second,third,fourth,fifth], axis=1)
            return final
        else:
            return -1

    if model == 3:
        year1 = existsInData( prunedData, team, year - 1)
        year2 = existsInData( prunedData, team, year - 2)
        year3 = existsInData( prunedData, team, year - 3)
        if year1 != -1 and year2 != -1 and year3 != -1:
            #get all 3 previous years
            first = exampleData.loc[[year1]]
            second = exampleData.loc[[year2]]
            third = exampleData.loc[[year3]]
            #reset indexes on previous years
            first.reset_index(drop=True,inplace=True)
            second.reset_index(drop=True,inplace=True)
            third.reset_index(drop=True,inplace=True)

            #concatinate all previous years
            final = pd.concat([first,second,third], axis=1)
            return final
        else:
            return -1

    if model == 1:
        year1 = existsInData( prunedData, team, year - 1)
        if year1 != -1:
            #get all 1 previous years
            first = exampleData.loc[[year1]]

            #reset indexes on previous years
            first.reset_index(drop=True,inplace=True)

            #concatinate all previous years
            final = pd.concat([first], axis=1)
            return final
        else:
            return -1

    if model == 0:
        year1 = existsInData( prunedData, team, year)
        if year1 != -1:

            #drop W/L/G
            exampleData = exampleData[["Rank","G",
                    "Ghome", "R", "AB",
                    "H", "2B", "3B", "HR", "BB", "SO", "SB", "CS",
                    "RA", "ER", "ERA", "CG", "SHO", "SV", "IPouts", "HA", "HRA",
                    "BBA", "SOA", "E", "DP", "FP", "attendance", "BPF", "PPF"]]
            
            #get all 1 previous years
            first = exampleData.loc[[year1]]

            #reset indexes on previous years
            first.reset_index(drop=True,inplace=True)

            #concatinate all previous years
            final = pd.concat([first], axis=1)
            return final
        else:
            return -1


'''
Gets the predicted wins for a specific year and team name for the specified model
team = team name
year = year that you want wins for
model = one of the folowing (5years = 5, 3years = 3, 1year = 1, sameYear = 0)

returns tuple of predicted wins or -1 if we dont have data for that year
and actual wins or -1 if we dont have data for that year
'''

def predict(team, year, model):

    conn = sqlite3.connect('flaskr/saved_models/lahman2016.sqlite')

    # Querying Database for all seasons where a team played 150 or more games and is still active today. 
    query = '''select * from Teams 
    inner join TeamsFranchises
    on Teams.franchID == TeamsFranchises.franchID
    where Teams.G >= 150 and TeamsFranchises.active == 'Y';
    '''

    # Convert results to DataFrame
    allData = pd.read_sql_query(query, conn)

    prunedData = allData[["yearID","franchID","divID","Rank","G",
                    "Ghome","W","L","DivWin","WCWin","LgWin","WSWin", "R", "AB",
                    "H", "2B", "3B", "HR", "BB", "SO", "SB", "CS", 
                    "RA", "ER", "ERA", "CG", "SHO", "SV", "IPouts", "HA", "HRA",
                    "BBA", "SOA", "E", "DP", "FP", "attendance", "BPF", "PPF"]]

    prunedData = prunedData.dropna()


    vector = getFeatureVector(team, year, model)
    if isinstance(vector, int):
        return -1

    #loads model and scalers based on the model used
    if model == 5:
        model = load_model('flaskr/saved_models/5yearModel.h5')
        scalerY = joblib.load('flaskr/saved_models/5yearModelYscaler.save')
        scalerX = joblib.load('flaskr/saved_models/5yearModelXscaler.save')

    if model == 3:
        model = load_model('flaskr/saved_models/3yearModel.h5')
        scalerY = joblib.load('flaskr/saved_models/3yearModelYscaler.save')
        scalerX = joblib.load('flaskr/saved_models/3yearModelXscaler.save')

    if model == 1:
        model = load_model('flaskr/saved_models/1yearModel.h5')
        scalerY = joblib.load('flaskr/saved_models/1yearModelYscaler.save')
        scalerX = joblib.load('flaskr/saved_models/1yearModelXscaler.save')

    if model == 0:
        model = load_model('flaskr/saved_models/singleModel.h5')
        scalerY = joblib.load('flaskr/saved_models/singleModelYscaler.save')
        scalerX = joblib.load('flaskr/saved_models/singleModelXscaler.save')

    #transform the input; scale and then transform the output
    transformedVector = scalerX.transform(vector)
    prediction = model.predict(transformedVector)
    prediction = scalerY.inverse_transform(prediction)

    #get the actual number of years
    actualYear = existsInData( prunedData, team, year)
    actual = -1
    if actualYear != -1:
        actual = prunedData.loc[[actualYear]]['W']

    return (prediction[0][0], actual.iloc[0])

    
