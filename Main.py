import sys
import pandas as pd
import os
import numpy as np
import csv
from InputProcessor import InputProcessor
from DictionaryCreator import DictionaryCreator


if __name__ == "__main__":

    arguments = sys.argv
    anEncoding = 'cp1252'
    trainingAddress = arguments[1]

    Input_Processor = InputProcessor()
    df_list = Input_Processor.read_file(trainingAddress, anEncoding)

    #for c, v, v2 in zip(list(df_list[0].columns.values), list(df_list[0].loc[1]), list(df_list[0].loc[2])):
        #print(c, " : ",  v, " | ", v2)

    #df = pd.DataFrame(df_list[0])
    #print(df.head())

   #--***--
    training_DictionaryCreator = DictionaryCreator()
    training_main_dictionary = training_DictionaryCreator.create_main_dictionary(df_list)
    training_min_dictionary = training_DictionaryCreator.create_min_dictionary()
    training_max_dictionary = training_DictionaryCreator.create_max_dictionary()
    temp = training_DictionaryCreator.create_acc_remain_predict_dictionary(df_list, 691200)

    training_acc_dictionary = temp[0]
    training_predictNaive_dictionary = temp[1]
    training_remain_dictionary = temp[2]

    for key, value in training_acc_dictionary.items():
        print(key, value)
