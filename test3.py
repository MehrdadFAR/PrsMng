import sys
import pandas as pd
import os

if __name__ == "__main__":

    arguments = sys.argv
    
    # This block checks if three arguments are provided, and assigns them to variables.
    if len(arguments) < 4:
        raise Exception("Provide three arguments: Address_Input Address_Test OutputName.csv")
    elif len(arguments) == 4:
        training = open(arguments[1]) # arguments[1] is the absolute path to the training input file
        # test = open(arguments[2]) # arguments[2] is the absolute path to the test input file
        outputName = arguments[3] # name of the output file
    else:
        pass # TO_DO: implementation of fetching extra variables.

    # If output name does not end with .csv or .txt append to it .csv
    if not (outputName.endswith(".csv") or outputName.endswith(".txt")):
        outputName = outputName + ".csv"
    
    # Read the CSV file
    inData = pd.read_csv(training)
    print(inData.head()) # TO_DO: REMOVE before dispatch

    # Add extra column for naive predictor
    inData['Naive_Predictor'] = 0 # TO_DO: "0" to be replaced with actual prediction
    print(inData.head()) # TO_DO: REMOVE before dispatch

    # Output the result a file
    inData.to_csv(outputName, index=False)

