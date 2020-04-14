import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from control_variables import create_data
from data_12_16 import return_sentiment
from data_00_08 import return_sentiment2
from sklearn.neighbors import KNeighborsClassifier  
from scipy.spatial.distance import euclidean
from scipy.stats import mode
from sklearn.metrics import accuracy_score
import nltk
from sklearn.preprocessing import StandardScaler

#Calculates the totals for positive, negative and total sentiment words
def calc_totals(data,year):
    data_year = data[data['Election_Year']==year].reset_index()
    
    #Republican Candidate Totals: Positive words, Negative words, Total Sentiment
    R_pos = 0 
    R_neg = 0 
    R_sent = 0
    
    #Democatic Candidate Totals: Positive words, Negative words, Total Sentiment
    D_pos = 0
    D_neg = 0
    D_sent = 0
    
    #List to be returned
    totals = []
    
    #Calculate the totals for each candidate per election year
    for i in range(len(data_year)):
        if data_year['Affiliation'][i] == 'R':
            R_pos += data_year['Positive_Words'][i]
            R_neg += data_year['Negative_Words'][i]
            R_sent += data_year['Total_Sentiment'][i]
        else:
            D_pos += data_year['Positive_Words'][i]
            D_neg += data_year['Negative_Words'][i]
            D_sent += data_year['Total_Sentiment'][i]
    
    #Creates the list to be returned
    for i in range(len(set(data_year['Affiliation']))):
        if data_year['Affiliation'][i] == 'R':
            totals.append([data_year['Election_Year'][i],data_year['Candidate_Name'][i],0,R_pos,R_neg,R_sent])
        else:
            totals.append([data_year['Election_Year'][i],data_year['Candidate_Name'][i],1,D_pos,D_neg,D_sent])
    
    return totals

#Cleans DataFrame
def clean_data():
    #Grabs DataFrames from test12 and test1 !!! change names !!!
    sentiment_00_08 = return_sentiment2()
    sentiment_12_16 = return_sentiment()
    
    election_data = pd.concat([sentiment_00_08,sentiment_12_16],join='outer')
    #New list to be turned into DataFrame
    data = []
    
    #Creates List of Totals for new DataFrame
    for year in set(election_data["Election_Year"]):
        data += calc_totals(election_data,year)
    
    #Sorts/creates new DataFrame
    data.sort()
    data = pd.DataFrame(data, columns=['Election_Year','Candidate_Name','Affiliation','Positive_Words','Negative_Words','Total_Sentiment'])
    
    return data

#Creates and returns feature and target vectors
def create_vectors():
    #creates dataframe with total of positive, negative and sentiment words
    totals = clean_data()
    
    #Grabs DataFrame from data_notebook.py
    win_data = create_data()
    win_data.sort_values(['Year','Candidate'], axis = 0, inplace = True)
    
    feature_vector = []
    for i in range(len(totals)):
        feature_vector.append([totals['Election_Year'][i],
                               totals['Affiliation'][i],
                               totals['Positive_Words'][i],
                               totals['Negative_Words'][i],
                               totals['Total_Sentiment'][i],
                               win_data['Candidate Spending ($1mil)'][i],
                               win_data['Final Favorability Rating (%)'][i], 
                               win_data['Voting-Eligible Population Turnout (%)'][i]])
        
    target_vector = list(win_data['Election Result'])
    return feature_vector, target_vector

#Trains Data
def train(size):
    feature_vector,target_vector = create_vectors()
    x_train, x_test, y_train, y_test = train_test_split(feature_vector,target_vector, test_size=size)
    return x_train, x_test, y_train, y_test

#Calculates prediction
def predict(k,size,x_input=[]):
    x_train, x_test, y_train, y_test = train(size)
    scaler = StandardScaler()
    scaler.fit(x_train)
    
    if x_input == []:
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)
        classifier = KNeighborsClassifier(n_neighbors = k, weights = 'distance')
        classifier.fit(x_train,y_train)
        y_pred = classifier.predict(x_test)
        accuracy = accuracy_score(y_pred,y_test)
        return y_pred, accuracy, y_test
    else:
        x_train = scaler.transform(x_train)
        x_input = scaler.transform(x_input)
        classifier = KNeighborsClassifier(n_neighbors = k, weights = 'distance')
        classifier.fit(x_train,y_train)
        y_pred = classifier.predict(x_input)
        return y_pred, x_input

    