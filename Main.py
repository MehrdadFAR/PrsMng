import sys
import pandas as pd
import os
import numpy as np
import csv
from InputProcessor import InputProcessor
from DictionaryCreator import DictionaryCreator
from NaiveEstimator import NaiveEstimator
from Visualization import Visualization
from ColumnCreator import ColumnCreator




if __name__ == "__main__":

    arguments = sys.argv
    anEncoding = 'cp1252'

    if len(arguments) < 4:
        raise Exception("Provide three arguments: Address_Input Address_Test OutputName.csv")
    else:
        trainingAddress = arguments[1]  #
        testAddress = arguments[2]  # arguments[2] is the absolute path to the test input file
        outputName = arguments[3]  # name of the output file
        if len(arguments) == 5: #to manually override encoding.
            anEncoding = arguments[4]


    file_Processor = InputProcessor()
    df_list_Training = file_Processor.read_file(trainingAddress, anEncoding)
    df_list_Test = file_Processor.read_file(testAddress, anEncoding)

    #--*FOR TESTING SAKE*--
    #for c, v, v2 in zip(list(df_list[0].columns.values), list(df_list[0].loc[1]), list(df_list[0].loc[2])):
        #print(c, " : ",  v, " | ", v2)

    #df = pd.DataFrame(df_list[0])
    #print(df.head())

   #--*FOR TESTING SAKE*--

    training_DictionaryCreator = DictionaryCreator()
    training_main_dictionary = training_DictionaryCreator.create_main_dictionary(df_list_Training)
    training_min_dictionary = training_DictionaryCreator.create_min_dictionary()
    training_max_dictionary = training_DictionaryCreator.create_max_dictionary()
    Naive_estimator_calculator = NaiveEstimator() #instantiate the object
    Naive_estimator_value = Naive_estimator_calculator.train_naive_estimator(training_min_dictionary, training_max_dictionary)

    test_DictionaryCreator = DictionaryCreator()
    test_main_dictionary = training_DictionaryCreator.create_main_dictionary(df_list_Test)
    test_min_dictionary = training_DictionaryCreator.create_min_dictionary()
    test_max_dictionary = training_DictionaryCreator.create_max_dictionary()
    print("training dictionaries created")

    temp = test_DictionaryCreator.create_acc_remain_predict_dictionary(df_list_Test, Naive_estimator_value)
    test_acc_dictionary = temp[0]
    test_predictNaive_dictionary = temp[1]
    test_remain_dictionary = temp[2]
    print("testing dictionaries created")

    print("this is the key - value" , test_predictNaive_dictionary['44964012621824'])

    a_column_creator = ColumnCreator()
    df_list_one_extra_col = a_column_creator.createExtraColumn(df_list_Test, test_predictNaive_dictionary)

    file_Processor.write_file(outputName, anEncoding, df_list_one_extra_col)

    visualizer = Visualization()
    naive_graph = visualizer.create_visualization(test_acc_dictionary, test_remain_dictionary, test_predictNaive_dictionary)
