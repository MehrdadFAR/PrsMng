import sys
import pandas as pd
import os

if __name__ == "__main__":

    training = open(sys.argv[1])
    test = open(sys.argv[2])
    output = sys.argv[3]
    inData = pd.read_csv(training)
    inData = inData.reindex( columns = inData.columns.tolist() + ["newColumn"])
    inData.to_csv(output)
    print(inData)
