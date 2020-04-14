#I compiled all of the data into a singular csv file (election_data.csv) and cleaned it up. This is all the code needed.

import pandas as pd

def create_data():
    election_data = pd.read_csv('election_data.csv') #Reading in the data

    for row in range(10,19):   #Dropping some extra rows
        election_data.drop(index = [row], inplace = True)
    
    election_data['Year'] = election_data['Year'].astype(int) #Making the year look nicer

    for i in range(len(election_data)):      #Changing the parties from the first letter to the full name
        if election_data.iloc[i,2] == 'R':
            election_data.iloc[i,2] = 'Republican'
        else:
            election_data.iloc[i,2] = 'Democrat'

    return election_data