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
from utilities.FileWriter import FileWriter
from estimators.NaiveModel import NaiveModel
from sklearn.cluster import KMeans
from utilities.MemoryUsage import MemoryUsage
from Visualization import Visualization
from estimators.Clustering import Clustering

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


    '''
    Train cluster estimator
    '''
    df_Training_copy2 = df_Training.copy()

    df_Test_copy2 = df_Test.copy()

    aClusterModel = Clustering()
    clustersTraining = aClusterModel.clusterData(trainingAddress, df_Training_copy2)
    clustersTest = aClusterModel.clusterData(trainingAddress, df_Test_copy2)

    naiveClass = NaiveModel()
    naiveClusterOne = naive_model.calc_naive_estimate(clustersTraining[0], clustersTest[0], a_file_finish_finder, trainingAddress)

    naiveClusterTwo = naive_model.calc_naive_estimate(clustersTraining[1], clustersTest[1], a_file_finish_finder, trainingAddress)

    naiveClusterThree = naive_model.calc_naive_estimate(clustersTraining[2], clustersTest[2], a_file_finish_finder, trainingAddress)

    naiveClusterFour = naive_model.calc_naive_estimate(clustersTraining[3], clustersTest[3], a_file_finish_finder, trainingAddress)

    naiveClusterFive = naive_model.calc_naive_estimate(clustersTraining[4], clustersTest[4], a_file_finish_finder, trainingAddress)


    clustered_estimations = clustered_estimations.append(naiveClusterOne)
    clustered_estimations = clustered_estimations.append(naiveClusterTwo)
    clustered_estimations = clustered_estimations.append(naiveClusterThree)
    clustered_estimations = clustered_estimations.append(naiveClusterFour)
    clustered_estimations = clustered_estimations.append(naiveClusterFive)

    #update filewriter to write column clustered estimator

    print(len(clustered_estimations))

    # Visualization

    ''' 
    print("Pre visualization")
    visualizer = Visualization()
    naive_graph = visualizer.create_visualization(naive_estimations)
    
    print("Finished visualization")
    '''
    a_file_writer = FileWriter(anEncoding)
    outputFile = a_file_writer.writeFile(outputName, df_Test, naive_estimations)
