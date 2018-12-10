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

def existsInData( df, team, year):
    #checks if a row with the correct team and year exists in the given datafram
    #returns the index of the row (or -1 if no row is found)
    for index, row in df.iterrows():
        if row["franchID"].iloc[0] == team and row["yearID"] == year:
            return index
    return -1


conn = sqlite3.connect('lahman2016.sqlite')

# Querying Database for all seasons where a team played 150 or more games and is still active today. 
query = '''select * from Teams 
inner join TeamsFranchises
on Teams.franchID == TeamsFranchises.franchID
where Teams.G >= 150 and TeamsFranchises.active == 'Y';
'''

# Convert results to DataFrame
allData = pd.read_sql_query(query, conn)

#pruning out wierd sections of data
prunedData = allData[["yearID","franchID","divID","Rank","G",
                "Ghome","W","L","DivWin","WCWin","LgWin","WSWin", "R", "AB",
                "H", "2B", "3B", "HR", "BB", "SO", "SB", "CS", 
                "RA", "ER", "ERA", "CG", "SHO", "SV", "IPouts", "HA", "HRA",
                "BBA", "SOA", "E", "DP", "FP", "attendance", "BPF", "PPF"]]

prunedData = prunedData.dropna()

#the statistics we use for vectors in each of the prevoius years
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

#the dataframes that we plan to fill 
finalX = pd.DataFrame()
finalY = pd.DataFrame()

#fills up a row with the vectors for every year that we have wins for
for index, row in prunedData.iterrows():
    year1 = existsInData( prunedData, row["franchID"].iloc[0], row["yearID"] - 1)
    year2 = existsInData( prunedData, row["franchID"].iloc[0], row["yearID"] - 2)
    year3 = existsInData( prunedData, row["franchID"].iloc[0], row["yearID"] - 3)
    year4 = existsInData( prunedData, row["franchID"].iloc[0], row["yearID"] - 4)
    year5 = existsInData( prunedData, row["franchID"].iloc[0], row["yearID"] - 5)
    #makes sure we have data from the previous years
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
        print(row)
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

        #combine the years into the final feature vector
        final = pd.concat([first,second,third,fourth,fifth], axis=1)
        finalX = pd.concat([finalX,final], ignore_index=True)
        y = exampleData.loc[[index]]['W']
        finalY = pd.concat([finalY,y], ignore_index=True)
        
        #print(finalX)
        #print(finalY)

        #input('')

        #print how far we are through the data
        print(index)
        
#finalX.to_pickle('1YearsX.pkl')
#finalY.to_pickle('1YearsY.pkl')


