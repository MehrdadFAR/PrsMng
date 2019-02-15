import sys
import pandas as pd
import os
import numpy as np

if __name__ == "__main__":

    arguments = sys.argv
    anEncoding = 'cp1252'

    # This block checks if three arguments are provided, and assigns them to variables.
    if len(arguments) < 4:
        raise Exception("Provide three arguments: Address_Input Address_Test OutputName.csv")
    else:
        trainingAddress = arguments[1]  #
        testAddress = arguments[2]  # arguments[2] is the absolute path to the test input file
        outputName = arguments[3]  # name of the output file
        if len(arguments) == 5:
            encoding = arguments[4]

    # If output name does not end with .csv or .txt append to it .csv
    if not (outputName.endswith(".csv") or outputName.endswith(".txt")):
        outputName = outputName + ".csv"
    
    # Read the CSV file
    inData = pd.read_csv(trainingAddress, encoding=anEncoding, low_memory=False)
    inDataTest = pd.read_csv(testAddress, encoding=anEncoding, low_memory=False)
    #print(inData.head()) # TO_DO: REMOVE before dispatch

    print(inDataTest.head())
    # Converting String to datetime
    timestamp = inData.columns.get_loc("event time:timestamp")
    inData[inData.columns[timestamp]] = pd.to_datetime(inData[inData.columns[timestamp]], format='%d-%m-%Y %H:%M:%S.%f')

    # Grouping cases by start and end time
    start_end_log = inData.groupby('case concept:name')['event time:timestamp'].apply(list)

    # Computing the delta
    delta = []
    counter = 0
    
    for i in start_end_log:
        first = i[0]
        last = i[-1]
        delta[counter] = last - first
        counter += 1

    #print('delta: ', delta)
    # Naive estimator ouput
    Estimation = np.mean(delta)
    secEstimation = Estimation / np.timedelta64(1, 's')
    #print(Estimation)
    
    # Converting String to datetime
    timestampTest = inDataTest.columns.get_loc("event time:timestamp")
    inDataTest[inDataTest.columns[timestampTest]] = pd.to_datetime(inDataTest[inDataTest.columns[timestamp]], format='%d-%m-%Y %H:%M:%S.%f')

    # Grouping cases by start and end time
    start_end_log_test = inDataTest.groupby('case concept:name')['event time:timestamp'].apply(list)

    dictionary = {}
    rowTracker = 0
    keyTracker = start_end_log_test.keys()

    for row in start_end_log_test:
        dict1 = {}
        # get input row in dictionary format
        # key = col_name

        # print(row) #This will print the whole row can be used for checking whether you actualy find the correct max.

        varKey = keyTracker[rowTracker]  # stores the key for the dictonary

        varMax = max(start_end_log_test.iloc[rowTracker])  # Var that keeps track of highest timestamp
        varMin = min(start_end_log_test.iloc[rowTracker])  # Var that keeps track of lowest timestamp
        temp1 = (varMax - varMin) / np.timedelta64(1,
                                                   's')  # Variable that holds difference in seconds between highest and lowest timestamp
        temp2 = secEstimation - temp1  # Variable that keeps track of estimate of remainder runtime event
        temp3 = max(0, temp2)  # makes sure remainder time is not negative

        # print(temp3)

        dict1.update({varKey: temp3})
        rowTracker += 1

        dictionary.update(dict1)
    #print(dictionary)


    # Add extra column for naive predictor
    inDataTest['Naive_Predictor'] = 0 #dictionary[] # TO_DO: "0" to be replaced with actual prediction


    rowsProcessed = 0
    for index, row in inDataTest.iterrows():
        inDataTest.at[rowsProcessed,'Naive_Predictor'] = dictionary[inDataTest.at[rowsProcessed,'case concept:name']]
        rowsProcessed += 1

    print(inDataTest.head()) # TO_DO: REMOVE before dispatch

    # Output the result a file
    inDataTest.to_csv(outputName, index=False)

