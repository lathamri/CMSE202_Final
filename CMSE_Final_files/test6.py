import pandas as pd
import numpy as np
import nltk
nltk.download('stopwords')

#Part 0: Import Speech Data
debate = open("Obama_McCain_101508.txt", encoding="utf8").read().split()
positive = open("positive-words.txt", encoding="utf8").read().split()
negative = open("negative-words.txt", encoding="utf8").read().split()

#Part 1: Separation Of Moderator, And The Two Candidates
mod_list = []
can1_list = []
can2_list = []

i_new = -1
i_old = -1
while i_new >= -len(debate):
    if debate[i_new] == 'SCHIEFFER:':
        mod_list += debate[i_new:]
        del debate[i_new:i_old]
        i_old = i_new

    elif debate[i_new] == 'OBAMA:':
        can1_list += debate[i_new:]
        del debate[i_new:i_old]
        i_old = i_new

    elif debate[i_new] == 'MCCAIN:':
        can2_list += debate[i_new:]
        del debate[i_new:i_old]
        i_old = i_new

    else: pass
    i_new -= 1

#Part 2: Removal Of Stop Words
stop_words = nltk.corpus.stopwords.words('english')
can1_list = [x for x in can1_list if x not in stop_words]
can2_list = [x for x in can2_list if x not in stop_words]

#Part 3: Sentiment Analysis
can1_pos = [x for x in can1_list if x in positive]
can1_neg = [x for x in can1_list if x in negative]
can2_pos = [x for x in can2_list if x in positive]
can2_neg = [x for x in can2_list if x in negative]

print('Candidate One Total Positive:', len(can1_pos))
print('Candidate Two Total Positive:', len(can2_pos))
print('Candidate One Total Negative:', len(can1_neg))
print('Candidate Two Total Negative:', len(can2_neg))
print('Candidate One Total Sentiment:', len(can1_pos)+len(can1_neg))
print('Candidate Two Total Sentiment:', len(can2_pos)+len(can2_neg))

def sentiment():
    Sentiment = pd.read_csv('SentimentData_00-08.csv')
    return Sentiment