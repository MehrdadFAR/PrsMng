import pandas as pd
from datetime import datetime, time
import numpy as np

# Importing data
data = pd.read_csv('training2017.csv', encoding='cp1252')

# Converting String to datetime
timestamp = data.columns.get_loc("event time:timestamp")
data[data.columns[timestamp]] = pd.to_datetime(data[data.columns[timestamp]], format='%d-%m-%Y %H:%M:%S.%f')

# Grouping cases by start and end time
start_end_log = data.groupby('case concept:name')['event time:timestamp'].apply(list)

# Computing the delta
delta = []

for i in start_end_log:
    first = i[0]
    last = i[-1]
    delta = last - first

# Naive estimator ouput
Estimation = np.mean(delta)
secEstimation = Estimation / np.timedelta64(1, 's')

rows_list = []
rowTracker = 0
keyTracker = start_end_log.keys()

for row in start_end_log:
    dict1 = {}
    # get input row in dictionary format
    # key = col_name

    # print(row) #This will print the whole row can be used for checking whether you actualy find the correct max.

    varKey = keyTracker[rowTracker] #stores the key for the dictonary

    varMax = max(start_end_log.iloc[rowTracker])  # Var that keeps track of highest timestamp
    varMin = min(start_end_log.iloc[rowTracker])  # Var that keeps track of lowest timestamp
    temp1 = (varMax - varMin) / np.timedelta64(1,'s')  # Variable that holds difference in seconds between highest and lowest timestamp
    temp2 = temp1 - secEstimation  # Variable that keeps track of estimate of remainder runtime event
    temp3 = max(0, temp2)  # makes sure remainder time is not negative

    #print(temp3)

    dict1.update({varKey : temp3})
    rowTracker += 1

    rows_list.append(dict1)
print(rows_list)
