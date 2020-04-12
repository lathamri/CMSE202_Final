{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "\n",
    "def create_data():\n",
    "    election_data = pd.read_csv('election_data.csv') #Reading in the data\n",
    "\n",
    "    for row in range(10,19):   #Dropping some extra rows\n",
    "        election_data.drop(index = [row], inplace = True)\n",
    "    \n",
    "    election_data['Year'] = election_data['Year'].astype(int) #Making the year look nicer\n",
    "\n",
    "    for i in range(len(election_data)):      #Changing the parties from the first letter to the full name\n",
    "        if election_data.iloc[i,2] == 'R':\n",
    "            election_data.iloc[i,2] = 'Republican'\n",
    "        else:\n",
    "            election_data.iloc[i,2] = 'Democrat'\n",
    "\n",
    "    return election_data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
