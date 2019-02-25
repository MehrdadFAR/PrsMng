import sys
import pandas as pd
import os
import numpy as np
import csv
from FileProcessorM import FileProcessorM
from DictionaryCreator import DictionaryCreator
from NaiveEstimator import NaiveEstimator
from Visualization import Visualization
from ColumnCreator import ColumnCreator
#from multiprocessing import Process
#import threading
#import datetime

from datetime import datetime

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

    if not (outputName.endswith(".csv") or outputName.endswith(".txt")):
        outputName = outputName + ".csv"

    finishing_event_list = None

    if  "dummy" in trainingAddress:
        finishing_event_list = ['e3','e4']
    elif  "BPI_2012" in trainingAddress:
        finishing_event_list = None
    elif  "BPI_2017" in trainingAddress:
        finishing_event_list = None
    elif "BPI_2018" in trainingAddress:
        finishing_event_list = ['case rejected', "case basic payment"]


    if finishing_event_list == None:
        raise Exception("finishing_events are not determined")

    def isFinishEvent(eventName):
        if eventName in finishing_event_list:
            return True
        else:
            return False

    naive_estimations = []
    #
    def predict_naive_estimation(test_evt, test_evt_caseName, test_Dict, train_Dict):
        test_evt_start_timeStamp = test_Dict[test_evt_caseName][1]
        test_evt_passed_time = (test_evt['event time:timestamp'] - test_evt_start_timeStamp).total_seconds()
        sum_finish_times  = 0
        count = 0
        for training_evt_dic in train_Dict.values():
            if training_evt_dic[2] != None:
                a_finish_time = training_evt_dic[2] - training_evt_dic[1]
                sum_finish_times += a_finish_time.total_seconds()
                count += 1
        if count == 0:
            pass
        else:
            estimate_finish_time = sum_finish_times / count
            estimate_remaining =  max(estimate_finish_time - test_evt_passed_time, 0)
            naive_estimations.append([test_evt['eventID '], estimate_remaining,
                                      test_evt_start_timeStamp,
                                      None])


        #if (predicted_finish_t_stamp == -2):
            #pass
        #else:
            #actual_days_past = test_evt_ts - test_case_start_ts
            #naive_estimation_remaining_days = max(predicted_finish_t_stamp - test_case_start_ts)
            #ns = (test_evt_case, actual_days_past, naive_estimation_remaining_days)
           # naive_estimations.append(ns)

            #predicted_total_finish_time  =  predicted_finish_t_stamp - test_case_start_ts
            #test_evt_time = test_evt['event time:timestamp']



    TrainingFile_Processor = FileProcessorM()
    TestingFile_Processor = FileProcessorM()
    #a_NaiveEstimator = NaiveEstimator()

    itt_train_file = TrainingFile_Processor.read_file(trainingAddress, anEncoding)
    itt_test_file =  TestingFile_Processor.read_file(testAddress, anEncoding)

    train_Dict = {}
    test_Dict = {}
    notFuture = True
    is_end_training =  False
    try:
        onHand_training_evt = next(itt_train_file)
    except StopIteration:
        is_end_training   = False


    for test_evt in itt_test_file:
        notFuture =  True
        test_evt_caseName = str([test_evt["case concept:name"]])
        test_evt_timeStamp = test_evt['event time:timestamp']
        #  if caseName is not in dict,  initialize with array [ [], case_start_stamp,
        #  case_finish_stamp].
        #  case_finish_stamp =   -1 means the case finsh time has not been determined yet.
        test_Dict.setdefault(test_evt_caseName, [[], test_evt_timeStamp, -1])[0].append(test_evt)

        while notFuture and not is_end_training:
            onHand_training_evt_timeStamp = onHand_training_evt['event time:timestamp']

            if onHand_training_evt_timeStamp <= test_evt_timeStamp:
                notFuture = True
                onHand_training_evt_caseName = str([onHand_training_evt["case concept:name"]])

                train_Dict_onHand_training_evt = train_Dict.setdefault(
                    onHand_training_evt_caseName, [[], onHand_training_evt_timeStamp, None])

                if isFinishEvent(onHand_training_evt["event concept:name"]):
                    train_Dict_onHand_training_evt[2] = onHand_training_evt_timeStamp
                    train_Dict_onHand_training_evt[0].append(onHand_training_evt)
                #progress to the next training event
                try:
                    onHand_training_evt = next(itt_train_file)
                except StopIteration:
                    is_end_training = True
                    break
            else:
                notFuture = False

        # assert: we have seen all the training events with time_stamp before or equal time_stamp
        # of the test_event.
        predict_naive_estimation(test_evt, test_evt_caseName, test_Dict, train_Dict)

    for key,value in test_Dict.items():
        print(key," : " ,value)
    print()
    for key,value in train_Dict.items():
        print(key," : " ,value)

    print(naive_estimations)
    print("Completed")

            #print(t1[1])
    #a_NaiveEstimator.calculate_naive_estimator()


    #list_df_Test = file_Processor.read_file(testAddress, anEncoding)

    #--*FOR TESTING SAKE*--
    #for c, v, v2 in zip(list(df_list[0].columns.values), list(df_list[0].loc[1]), list(df_list[0].loc[2])):
        #print(c, " : ",  v, " | ", v2)

    #df = pd.DataFrame(df_list[0])
    #print(df.head())

   #--*FOR TESTING SAKE*--

    #training_DictionaryCreator = DictionaryCreator()
    #training_main_dictionary = training_DictionaryCreator.create_main_dictionary(list_df_Training)
    #training_min_dictionary = training_DictionaryCreator.create_min_dictionary()
    #training_max_dictionary = training_DictionaryCreator.create_max_dictionary()
    #Naive_estimator_calculator = NaiveEstimator() #instantiate the object
    #Naive_estimator_value = Naive_estimator_calculator.train_naive_estimator(training_min_dictionary, training_max_dictionary)

    #test_DictionaryCreator = DictionaryCreator()
    #test_main_dictionary = training_DictionaryCreator.create_main_dictionary(list_df_Test)
    #test_min_dictionary = training_DictionaryCreator.create_min_dictionary()
    #test_max_dictionary = training_DictionaryCreator.create_max_dictionary()
    #print("training dictionaries created")

    #temp = test_DictionaryCreator.create_acc_remain_predict_dictionary(list_df_Test, Naive_estimator_value)
    #test_acc_dictionary = temp[0]
    #test_predictNaive_dictionary = temp[1]
    #test_remain_dictionary = temp[2]
    #print("testing dictionaries created")

    #print(test_predictNaive_dictionary['45011257262090'])

    #a_column_creator = ColumnCreator()
    #list_df_extra_col = a_column_creator.createExtraColumn(list_df_Test, test_predictNaive_dictionary)

    #file_Processor.write_file(outputName, anEncoding, list_df_extra_col)

    #visualizer = Visualization()
    #naive_graph = visualizer.create_visualization(test_acc_dictionary, test_remain_dictionary, test_predictNaive_dictionary)

