import sys
import time

# import csv
# from DictionaryCreator import DictionaryCreator
# from NaiveEstimator import NaiveEstimator
# from Visualization import Visualization
# from ColumnCreator import ColumnCreator
# from multiprocessing import Process
# import threading
# import datetime
import pandas as pd
from V4.utilities.ArgumentProcessor import ArgumentProcessor
from V4.utilities.FileFinishFinder import FileFinishFinder
from V4.utilities.FileReader import FileReader
from V4.utilities.FileWriter import FileWriter
from V4.estimators.NaiveModel import NaiveModel
from V4.utilities.MemoryUsage import MemoryUsage
from V4.utilities.Visualization import Visualization
from V4.estimators.StateDiagramModel import State_Diagram_Model

if __name__ == "__main__":

    arguments = sys.argv

    ''' 
    Process the command line arguments
    '''
    AP = ArgumentProcessor()
    trainingAddress, testAddress, outputName, anEncoding = AP.processArgs(arguments)


    '''
    an instance of FileFinishFinder. Used to find finishing event names.
    '''
    a_file_finish_finder = FileFinishFinder(trainingAddress)

    '''
    Initialize the FileReader with encoding. The method  readFile(address) reads the input and returns a 
    pandas Data Frame. 
    '''
    a_file_reader = FileReader(anEncoding)

    t1 = time.time()
    df_Training_original = a_file_reader.readFile(trainingAddress)
    df_Training_original['event time:timestamp'] = pd.to_datetime(df_Training_original['event time:timestamp'], dayfirst=True, infer_datetime_format=True)
    print("time _ read training file: "+ str("%.0f" % (time.time() - t1)) + "  sec")

    t1 = time.time()
    df_Test_original = a_file_reader.readFile(testAddress)
    df_Test_original['event time:timestamp'] = pd.to_datetime(df_Test_original['event time:timestamp'], dayfirst=True, infer_datetime_format=True)

    print("time _ read test file: " + str("%.0f" % (time.time() - t1)) + "  sec")
    print("memory usage of training DF (in MegaBytes): ", MemoryUsage.memory_usage_sum(df_Training_original))
    print("memory usage of test DF (in MegaBytes): ", MemoryUsage.memory_usage_sum(df_Test_original))

    '''
    make a copy of data frames
    '''
    df_Training_extra = df_Training_original.copy()
    df_Test_extra = df_Test_original.copy()

    '''
    add event_stat column 
    '''
    if ("BPI_2012" in trainingAddress):
        df_Training_extra['EventStatus'] = \
            df_Training_extra['event concept:name'] + ' ' + df_Training_extra['event lifecycle:transition']
        df_Test_extra['EventStatus'] = \
            df_Test_extra['event concept:name'] + ' ' + df_Test_extra['event lifecycle:transition']
    else:
        df_Training_extra['EventStatus'] = df_Training_extra['event concept:name']
        df_Test_extra['EventStatus'] = df_Test_extra['event concept:name']


    '''
    Train naive estimator
    '''
    naive_model = NaiveModel()

    t1 = time.time()

    #naive_estimations = naive_model.calc_naive_estimate(df_Training_extra.copy(), df_Test_extra.copy(),
    #a_file_finish_finder, trainingAddress)

    t2 = time.time()
    print("Time _ calculating naive_estimation: " + str("%.0f" % (t2 - t1)) + "  sec")



    """ 
    Train State Transition estimator 
    """
    t1 = time.time()

    a_State_Diagram_Model = State_Diagram_Model()
    MAX_LENGTH = 2
    ST_estimations = a_State_Diagram_Model.calc_state_transition(df_Training_extra.copy(),
                                                                  df_Test_extra.copy(), a_file_finish_finder, MAX_LENGTH)

    t2 = time.time()
    print("Time _ calculating ST_estimation: " + str("%.0f" % (t2 - t1)) + "  sec")

    #print(ST_estimations)
    '''
    Visualization
    '''

    """ 
    for l in ST_estimations:
        if l[0] == 212172:
            print(l)
    """

    # start of visualization
    visualizer = Visualization()

    #naive_graph_scatter = visualizer.create_scatter(naive_estimations, "ST Estimator")
    ST_graph_scatter = visualizer.create_scatter(ST_estimations, "ST Estimator")

    # scatter plot for the clustered estimator
    #plotName = "ST Estimator"
    #ST_graph_scatter = visualizer.create_scatter(clustered_estimations, plotName)

    # prints the MSE diagrams
    #naive_graph_mse = visualizer.create_mse(naive_graph_scatter[0], naive_graph_scatter[1],
                                            #naive_graph_scatter[2], ST_graph_scatter[0],
                                            #ST_graph_scatter[1], ST_graph_scatter[2])
    #print("Finished visualization3")
