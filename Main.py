import sys
import pandas as pd
import os
import numpy as np
import csv
from InputProcessor import InputProcessor

if __name__ == "__main__":

    arguments = sys.argv
    anEncoding = 'cp1252'
    trainingAddress = arguments[1]

    Input_Processor = InputProcessor()
    df_list = Input_Processor.read_file(trainingAddress, anEncoding)



    print(list(df_list[0].columns.values))

    print(list(df_list[0].loc[1]))


    for c, v, v2 in zip(list(df_list[0].columns.values), list(df_list[0].loc[1]), list(df_list[0].loc[2])):
        print(c, " : ",  v, " | ", v2)

    df = pd.DataFrame(df_list[0])
    print(df.head())
