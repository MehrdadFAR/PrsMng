import sys
import pandas as pd
import os
import numpy as np
import csv
from InputProcessor import InputProcessor
from DictionaryCreator import DictionaryCreator
from NaiveEstimator import NaiveEstimator
from Visualization import Visualization




if __name__ == "__main__":

    arguments = sys.argv
    anEncoding = 'cp1252'

    #if len(arguments) < 4:
        #raise Exception("Provide three arguments: Address_Input Address_Test OutputName.csv")
    #else:
        #trainingAddress = arguments[1]  #
        #testAddress = arguments[2]  # arguments[2] is the absolute path to the test input file
        #outputName = arguments[3]  # name of the output file
        #if len(arguments) == 5: #to manually override encoding.
           # anEncoding = arguments[4]

    trainingAddress = arguments[1]


    Input_Processor = InputProcessor()
    df_list = Input_Processor.read_file(trainingAddress, anEncoding)

    #--*FOR TESTING SAKE*--
    #for c, v, v2 in zip(list(df_list[0].columns.values), list(df_list[0].loc[1]), list(df_list[0].loc[2])):
        #print(c, " : ",  v, " | ", v2)

    #df = pd.DataFrame(df_list[0])
    #print(df.head())

   #--*FOR TESTING SAKE*--

    training_DictionaryCreator = DictionaryCreator()
    training_main_dictionary = training_DictionaryCreator.create_main_dictionary(df_list)
    #for key, value in training_main_dictionary.items():
        #print(key, value)
    training_min_dictionary = training_DictionaryCreator.create_min_dictionary()
    training_max_dictionary = training_DictionaryCreator.create_max_dictionary()


    #print('max dic')
    #for key, value in training_max_dictionary.items():
        #print(key, value)
    Naive_estimator_training = NaiveEstimator()
    Naive_estimator = Naive_estimator_training.train_naive_estimator(training_min_dictionary, training_max_dictionary)
    #print(" THIS IS THE ESTIMATOR ", Naive_estimator)
    temp = training_DictionaryCreator.create_acc_remain_predict_dictionary(df_list, Naive_estimator)

    training_acc_dictionary = temp[0]
    training_predictNaive_dictionary = temp[1]
    training_remain_dictionary = temp[2]


    testing_visualization = Visualization()
    creating_graph = testing_visualization.create_visualization(training_acc_dictionary, training_remain_dictionary, training_predictNaive_dictionary)

    #--**for testing**--
    #for key, value in training_acc_dictionary.items():
        #print(key, value)
