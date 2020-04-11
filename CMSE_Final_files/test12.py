import numpy as np
import re
import nltk
nltk.download('stopwords')
import pandas as pd

class pre_process():
    """
    This class is designed to take a filename linking to a text file and return a cleaned list for processing.
    """
    def __init__(self, filename):
        """
        Take in a filename as a string to work on.
        """
        self.filename = filename
    
    def get_data(self):
        """
        Get our data from some txt file. This will be split by word to be.
        """
        # Load our txt file and split it by word
        self.data = open(self.filename).read().split()
        return self.data
    
    def seperate_speeches(self):
        """
        This splits our speeches into seperate lists depending on who is speaking.
        If new speeches are included you may input the names of the moderaters and speakers.
        It returns a list of three lists with all speaking points for each speaker contatenated.
        """
        debate = self.data
        mod_list = []
        can1_list = []
        can2_list = []

        i_new = -1
        i_old = -1
        while i_new >= -len(debate):
            if (debate[i_new] == 'LEHRER:' or debate[i_new] == 'CROWLEY:' or debate[i_new] == 'SCHIEFFER:'
              or debate[i_new] == 'HOLT:' or debate[i_new] == 'RADDATZ:'or debate[i_new] == 'WALLACE:'):
                mod_list += debate[i_new:]
                del debate[i_new:i_old]
                i_old = i_new

            elif debate[i_new] == 'OBAMA:' or debate[i_new] == 'CLINTON:':
                can1_list += debate[i_new:]
                del debate[i_new:i_old]
                i_old = i_new

            elif debate[i_new] == 'ROMNEY:' or debate[i_new] == 'TRUMP:':
                can2_list += debate[i_new:]
                del debate[i_new:i_old]
                i_old = i_new

            else:
                pass
            i_new -= 1
        
        speeches = (can1_list, can2_list)
        
        can_aslists = []
        for j in range(2):
            can_aslists.append(' '.join(speeches[j]))
        return can_aslists
    
    def clean(self, data):
        """
        Takes in our data and strips all unnecessary characters and names for efficiency.
        This step is not required for basic sentiment analysis in general, but is for more
        complex analysis.
        """
        # Characters to remove
        remove = re.compile(r"[\'\"\\\!\,\/\;\{\}\[\.\]]")
        remove_names = re.compile(r'(ROMNEY:) (OBAMA:) (LEHRER:) (CLINTON:) (SCHIEFFER:) (CRAWLEY:) (TRUMP:)')
        # List to store clean speeches
        removed_names = []
        clean_data = []
        # Loop over each speech and remove all regex excluded characters defined above
        for speech in data:
            remove_char = remove.sub("", speech)
            removed_names.append(remove_char)
        for speech in removed_names:
            clean_speech = remove_names.sub("", speech)
            clean_data.append(clean_speech)

        return clean_data
    
    def remove_stop_words(self, clean_speeches):
        """
        Use nltk stopwords to remove a subset of words from each space.
        The removed words take away very little context and so don't affect analysis, but 
        is much quicker to sort through for analysis.
        """
        stop_words = nltk.corpus.stopwords.words('english')
        removed_words_speeches = []
        for speech in clean_speeches:
            removed_words_speeches.append(' '.join([word for word in speech.split() if word not in stop_words]))
        return removed_words_speeches
    
    
class sentiment_analysis():
    """
    This class loads in our positive and negative words for our sentiment analysis and counts
    the good and bad sentiment words for each speech given.
    """
    def __init__(self, data):
        """
        Take in our data and store it.
        """
        self.data = data
    
    def read_good_bad(self, pos, neg):
        """
        Create a list containing the words with positive and negative sentiment.
        """
        self.pos = np.loadtxt(pos, dtype = str,encoding="ISO-8859-1")
        self.neg = np.loadtxt(neg, dtype=str ,encoding="ISO-8859-1")
        self.good_bad = [list(self.pos), list(self.neg)]
        return self.good_bad
    
    def sentiment_count(self, speech):
        """
        Count the good and bad sentiment words for each speech and return them as a tuple.
        """
        good_count = [x for x in speech if x in self.good_bad[0]]
        bad_count = [x for x in speech if x in self.good_bad[1]]
        return (good_count, bad_count)
    

def return_sentiment():
    Speech_list = ['Obama_Romeny_1.txt','Obama_Romeny_2.txt','Obama_Romeny_3.txt',
                    'Clinton_Trump_1.txt','Clinton_Trump_2.txt','Clinton_Trump_3.txt']
    good_list = 'positive-words.txt'
    bad_list = 'negative-words.txt'

    # Initialize temporary values for storing, indexing, and date placement.
    output = []
    i = 0
    j = 0
    Debate_Date = ['10/3/2012', '10/16/2012', '10/22/2012', '9/26/2016', '10/9/2016', '10/19/2016']

    # Loop over all speeches in the list above
    for val in Speech_list:
    
        # grab the speech
        data = pre_process(val)

        # extract the speeches data
        y = data.get_data()

        # seperate the speeches by speaker
        r = data.seperate_speeches()
    
        # clean each speech
        x = data.clean(r)

        # remove the stop words
        z = data.remove_stop_words(x)
    
        # initialize our analysis on the cleaned speech
        SA = sentiment_analysis(z)
        
        # grab our positive and negative sentiment list
        SA.read_good_bad(good_list, bad_list)
        
        # loop over each speaker in the speech
        for q in range(len(z)):
            # finds out who is speaking based on indexing
            if i==0 or i==1 or i==2:
                # Democrates come first 
                if q==0:
                    Candidate_Name = 'Barack Obama'
                    Affiliation = 'D'
                    Election_Year = 2012
                else:
                    Candidate_Name = 'Mitt Romney'
                    Affiliation = 'R'
                    Election_Year = 2012
            if i==3 or i==4 or i==5:
                if q==0:
                    Candidate_Name = 'Hillary Clinton'
                    Affiliation = 'D'
                    Election_Year = 2016
                else:
                    Candidate_Name = 'Donald Trump'
                    Affiliation = 'R'
                    Election_Year = 2016
            # split our speeches by word to perform analysis
            y = SA.sentiment_count(z[q].split())
            good = len(y[0])
            bad = len(y[1])
        
            # return the prefered data.
            output.append([Election_Year, Debate_Date[j], Candidate_Name, Affiliation, good, bad, good+bad])
        i += 1
        j += 1
 
    #Create it as a Pandas DataFrame
    sentiment_12_16 = pd.DataFrame(output, columns=['Election_Year', 'Debate_Date', 'Candidate_Name', 'Affiliation', 'Positive_Words',         'Negative_Words', 'Total_Sentiment'])
    
    return sentiment_12_16