import sys
import pandas as pd
import os



def hello(a,b):
    print ("hello and that's your sum:", a + b)

if __name__ == "__main__":

    f = open("Road_Traffic_Fine_Management_Process-training.csv")
    output = "output.csv"
    inData = pd.read_csv(f)
    inData = inData.reindex( columns = inData.columns.tolist() + ["newColumn"])
    inData.to_csv(output)
    print(inData)
