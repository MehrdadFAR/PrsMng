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
from utilities.ArgumentProcessor import ArgumentProcessor
from utilities.FileFinishFinder import FileFinishFinder
from utilities.FileReader import FileReader
from estimators.NaiveModel import NaiveModel
from utilities.MemoryUsage import MemoryUsage
from Visualization import Visualization

if __name__ == "__main__":

    arguments = sys.argv

    ''' 
    Process the command line arguments
    '''
    AP = ArgumentProcessor()
    trainingAddress, testAddress, outputName, anEncoding = AP.processArgs(arguments)


    '''
    an object of FileFinishFinder, which is used to find finish event names.
    '''
    a_file_finish_finder = FileFinishFinder(trainingAddress)

    '''
    Initialize the FileReaderRead with encoding, use the objects readFile(address) method to 
    read the input files. This returns a pandas Data Frame. 
    '''
    a_file_reader = FileReader(anEncoding)
    t1 = time.time()
    df_Training = a_file_reader.readFile(trainingAddress)
    df_Training['event time:timestamp'] = pd.to_datetime(df_Training['event time:timestamp'], dayfirst=True, infer_datetime_format=True)
    #debugging
    print('after the time conversion of training')
    # monitoring time required to read the files:
    print("time _ read training file: "+ str("%.0f" % (time.time() - t1)) + "  sec")
    print("memory usage of training DF (in MegaBytes): ", MemoryUsage.memory_usage_sum(
        df_Training))
    t1 = time.time()
    df_Test = a_file_reader.readFile(testAddress)
    df_Test['event time:timestamp'] = pd.to_datetime(df_Test['event time:timestamp'], dayfirst=True, infer_datetime_format=True)
    # debugging
    print('after the time conversion of test')
    # monitoring time required to read the files:
    print("time _ read test file: " + str("%.0f" % (time.time() - t1)) + "  sec")


    '''
    Train naive estimator
    '''
    t1 = time.time()
    df_Training_copied = df_Training.copy()
    t2 = time.time()
    print("time to_ make a copy of DF Training: " + str("%.0f" % (t2 - t1)) + "  sec")

    t1 = time.time()
    df_Test_copied = df_Test.copy()
    t2 = time.time()
    print("time to_ make a copy of DF Training: " + str("%.0f" % (t2 - t1)) + "  sec")

    naive_model = NaiveModel()

    t1 = time.time()
    # naive_estimations is a list of dictionaries. Mutable,  do not change values.  Not
    # copied for memory saving purposes.
    naive_estimations = naive_model.calc_naive_estimate(df_Training_copied, df_Test_copied, a_file_finish_finder,
                                                        trainingAddress)
    t2 = time.time()
    print("Time _ calculating naive_estimation: " + str("%.0f" % (t2 - t1)) + "  sec")

    # Visualization

    print("Pre visualization")
    visualizer = Visualization()
    naive_graph = visualizer.create_visualization(naive_estimations)

    print("Finished visualization")
