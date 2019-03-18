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

    naiveClassOne = NaiveModel()
    naiveClusterOne = naiveClassOne.calc_naive_estimate(clustersTraining[0], clustersTest[0], a_file_finish_finder, trainingAddress)

    naiveClassTwo = NaiveModel()
    naiveClusterTwo = naiveClassTwo.calc_naive_estimate(clustersTraining[1], clustersTest[1], a_file_finish_finder, trainingAddress)

    naiveClassThree = NaiveModel()
    naiveClusterThree = naiveClassThree.calc_naive_estimate(clustersTraining[2], clustersTest[2], a_file_finish_finder, trainingAddress)

    naiveClassFour = NaiveModel()
    naiveClusterFour = naiveClassFour.calc_naive_estimate(clustersTraining[3], clustersTest[3], a_file_finish_finder, trainingAddress)

    naiveClassFive = NaiveModel()
    naiveClusterFive = naiveClassFive.calc_naive_estimate(clustersTraining[4], clustersTest[4], a_file_finish_finder, trainingAddress)


    clustered_estimations = []
    clustered_estimations.extend(naiveClusterOne)
    clustered_estimations.extend(naiveClusterTwo)
    clustered_estimations.extend(naiveClusterThree)
    clustered_estimations.extend(naiveClusterFour)
    clustered_estimations.extend(naiveClusterFive)


    #clustered_estimations = pd.concat([naiveClusterOne, naiveClusterTwo, naiveClusterThree, naiveClusterFour, naiveClusterFive])

    print("1 ", len(naiveClusterOne))
    print("2 ", len(naiveClusterTwo))
    print("3 ", len(naiveClusterThree))
    print("4 ", len(naiveClusterFour))
    print("5 ", len(naiveClusterFive))


    #update filewriter to write column clustered estimator

    print(len(clustered_estimations))

    # Visualization

    print(type(naive_estimations))
    print(type(clustered_estimations))

    print("naive ", naive_estimations[0])

    #print("clustered ", naiveClusterOne[0])

    print("clustered ", clustered_estimations[0])

    print("Pre visualization1")

    visualizer1 = Visualization()
    naive_graph = visualizer1.create_visualization(naive_estimations)
    
    print("Finished visualization1")

    print("Pre visualization2")
    visualizer2 = Visualization()
    clustered_graph = visualizer2.create_visualization(clustered_estimations)

    print("Finished visualization2")

    a_file_writer = FileWriter(anEncoding)
    outputFile = a_file_writer.writeFile(outputName, df_Test, naive_estimations, clustered_estimations)
