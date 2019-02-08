import sys
import pandas as pd
import os



def hello(a,b):
    print ("hello and that's your sum:", a + b)

if __name__ == "__main__":
    
    f = open(sys.argv[1])
    inData = pd.read_csv(f)
    print(inData)
