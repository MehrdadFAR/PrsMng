import sys
import time

import pandas as pd
from utilities.ArgumentProcessor import ArgumentProcessor
from utilities.FileFinishFinder import FileFinishFinder
from utilities.FileReader import FileReader
from utilities.FileWriter import FileWriter
from utilities.TestClusterer import TestClusterer
from utilities.ClusterAttributeFinder import ClusterAttributeFinder
from estimators.NaiveModel import NaiveModel
from utilities.MemoryUsage import MemoryUsage
from utilities.Visualization import Visualization
from utilities.ToDateTime import ToDateTime
from estimators.StateDiagramModel import State_Diagram_Model
from estimators.Clustering import Clustering

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
    data_file_name = a_file_finish_finder.get_data_file_name()

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

    """ 
    make a copy of data frames
    """
    df_Training_extra = df_Training_original.copy()
    df_Test_extra = df_Test_original.copy()

    """ 
    add event_stat column 
    """

    if ("BPI_2012" in trainingAddress):
        df_Training_extra['EventStatus'] = \
            df_Training_extra['event concept:name'] + ' ' + df_Training_extra['event lifecycle:transition']
        df_Test_extra['EventStatus'] = \
            df_Test_extra['event concept:name'] + ' ' + df_Test_extra['event lifecycle:transition']
    else:
        df_Training_extra['EventStatus'] = df_Training_extra['event concept:name']
        df_Test_extra['EventStatus'] = df_Test_extra['event concept:name']

    """
    Train naive estimator
    """
    '''
    naive_model = NaiveModel()

    t1 = time.time()

    naive_estimations = naive_model.calc_naive_estimate(df_Training_extra.copy(),
                                                        df_Test_extra.copy(), a_file_finish_finder, trainingAddress)

    t2 = time.time()
    print("Time _ calculating naive_estimation: " + str("%.0f" % (t2 - t1)) + "  sec")
'''
    """ 
    Train State Transition estimator 
    """
    '''
    t1 = time.time()

    a_State_Diagram_Model = State_Diagram_Model()
    MAX_LENGTH = a_file_finish_finder.get_max_lenght(trainingAddress)
    ST_estimations = a_State_Diagram_Model.calc_state_transition(df_Training_extra.copy(),
                                                                 df_Test_extra.copy(), a_file_finish_finder, MAX_LENGTH)

    t2 = time.time()
    print("Time _ calculating ST_estimation: " + str("%.0f" % (t2 - t1)) + "  sec")
    '''
    """
    Train cluster estimators
    """
    t1 = time.time()
    #aClusterFinderModel = ClusterAttributeFinder()
    #a_cluster_attribute = aClusterFinderModel.clusterAttributeDefiner(trainingAddress)

    df_Training_cluster = df_Training_extra.copy()
    df_Test_cluster = df_Test_extra.copy()

    aDateTimeModel = ToDateTime()

    df_Training_cluster = aDateTimeModel.toDateTime(df_Training_cluster)
    df_Test_cluster = aDateTimeModel.toDateTime(df_Test_cluster)

    aClusterModel = Clustering()
    clustersTraining = aClusterModel.clusterData(df_Training_cluster)
    clustersTest = aClusterModel.clusterData(df_Test_cluster)

    clusterNaiveModel = NaiveModel()
    naiveClusters = [0,0,0,0,0,0,0,0,0,0,0,0]
    clustered_estimations = []
    counter = 0
    for i in clustersTest:
        if isinstance(i, int):
            print('integer : ', i, "AND Counter = ", counter)
        if not i.empty:
            naiveClusters[counter] = clusterNaiveModel.calc_naive_estimate(clustersTraining[counter], clustersTest[counter], a_file_finish_finder, trainingAddress)
            clustered_estimations.append(naiveClusters[counter])
        counter += 1
    '''
    naiveClassOne = NaiveModel()
    naiveClusterOne = naiveClassOne.calc_naive_estimate(clustersTraining[0], clustersTest[0], a_file_finish_finder,
                                                        trainingAddress)

    naiveClassTwo = NaiveModel()
    naiveClusterTwo = naiveClassTwo.calc_naive_estimate(clustersTraining[1], clustersTest[1], a_file_finish_finder,
                                                        trainingAddress)

    naiveClassThree = NaiveModel()
    naiveClusterThree = naiveClassThree.calc_naive_estimate(clustersTraining[2], clustersTest[2], a_file_finish_finder,
                                                            trainingAddress)
    naiveClassFour = NaiveModel()
    naiveClusterFour = naiveClassFour.calc_naive_estimate(clustersTraining[3], clustersTest[3], a_file_finish_finder,
                                                          trainingAddress)

    naiveClassFive = NaiveModel()
    naiveClusterFive = naiveClassFive.calc_naive_estimate(clustersTraining[4], clustersTest[4], a_file_finish_finder,
                                                          trainingAddress)

    naiveClassSix = NaiveModel()
    naiveClusterSix = naiveClassSix.calc_naive_estimate(clustersTraining[5], clustersTest[5], a_file_finish_finder,
                                                          trainingAddress)

    naiveClassSeven = NaiveModel()
    naiveClusterSeven = naiveClassSeven.calc_naive_estimate(clustersTraining[6], clustersTest[6], a_file_finish_finder,
                                                          trainingAddress)

    naiveClassEight = NaiveModel()
    naiveClusterEight = naiveClassEight.calc_naive_estimate(clustersTraining[7], clustersTest[7], a_file_finish_finder,
                                                          trainingAddress)

    naiveClassNine = NaiveModel()
    naiveClusterNine = naiveClassNine.calc_naive_estimate(clustersTraining[8], clustersTest[8], a_file_finish_finder,
                                                          trainingAddress)

    naiveClassTen = NaiveModel()
    naiveClusterTen = naiveClassTen.calc_naive_estimate(clustersTraining[9], clustersTest[9], a_file_finish_finder,
                                                          trainingAddress)

    naiveClassEleven = NaiveModel()
    naiveClusterEleven = naiveClassEleven.calc_naive_estimate(clustersTraining[10], clustersTest[10], a_file_finish_finder,
                                                          trainingAddress)

    naiveClassTwelth = NaiveModel()
    naiveClusterTwelth = naiveClassTwelth.calc_naive_estimate(clustersTraining[11], clustersTest[11], a_file_finish_finder,
                                                          trainingAddress)
    '''

    '''
    clustered_estimations = []
    clustered_estimations.extend(naiveClusterOne)
    clustered_estimations.extend(naiveClusterTwo)
    clustered_estimations.extend(naiveClusterThree)
    clustered_estimations.extend(naiveClusterFour)
    clustered_estimations.extend(naiveClusterFive)
    clustered_estimations.extend(naiveClusterSix)
    clustered_estimations.extend(naiveClusterSeven)
    clustered_estimations.extend(naiveClusterEight)
    clustered_estimations.extend(naiveClusterNine)
    clustered_estimations.extend(naiveClusterTen)
    clustered_estimations.extend(naiveClusterEleven)
    clustered_estimations.extend(naiveClusterTwelth)
    '''
    t2 = time.time()
    print("Time _ calculating Cluster estimation: " + str("%.0f" % (t2 - t1)) + "  sec")
    """
    visualization
    """
    print("visualization started")

    visualizer = Visualization()

    # Shows the scatter plot for the naive estimator
    #plotName = "Naive Prediction"
    #naive_graph_scatter = visualizer.create_scatter(naive_estimations, plotName, data_file_name)

    # Shows the scatter plot for the clustered estimator
    plotName = "Clustered Prediction"
    clustered_graph_scatter = visualizer.create_scatter(clustered_estimations, plotName, data_file_name)

    # Shows the scatter plot for the ST estimator
    #ST_graph_scatter = visualizer.create_scatter(ST_estimations, "ST Estimator", data_file_name)
    
    print("Finished visualization of scatter plots")

    # prints the MSE diagrams
    visualizer2 = None
    if "BPI_2019" in trainingAddress:    
        visualizer2 = Visualization()

    if "BPI_2019" in trainingAddress:
        name = "MSE_1"
        #visualizer.create_mse(naive_graph_scatter[0], naive_graph_scatter[1], naive_graph_scatter[2])
        visualizer.create_mse(clustered_graph_scatter[0], clustered_graph_scatter[1], clustered_graph_scatter[2])
        #visualizer.create_mse(ST_graph_scatter[0], ST_graph_scatter[1], ST_graph_scatter[2])
        visualizer.finishMSE(name, trainingAddress)
        name = "MSE_2"
        visualizer2.create_mse(naive_graph_scatter[3], naive_graph_scatter[4], naive_graph_scatter[5])
        visualizer2.create_mse(clustered_graph_scatter[3], clustered_graph_scatter[4], clustered_graph_scatter[5])
        #visualizer2.create_mse(ST_graph_scatter[3], ST_graph_scatter[4], ST_graph_scatter[5])
        visualizer2.finishMSE(name, trainingAddress)

    else:
        name = "MSE"
        #visualizer.create_mse(naive_graph_scatter[0], naive_graph_scatter[1], naive_graph_scatter[2])
        visualizer.create_mse(clustered_graph_scatter[0], clustered_graph_scatter[1], clustered_graph_scatter[2])
        #visualizer.create_mse(ST_graph_scatter[0], ST_graph_scatter[1], ST_graph_scatter[2])
        visualizer.finishMSE(name, trainingAddress)
    print("Finished visualization of MSE")

    """
    Writes the estimators to the output file ST SHOULD STILL BE ADDED
    """
    #a_file_writer = FileWriter(anEncoding)
    #outputFile = a_file_writer.writeFile(outputName, df_Test_original, naive_estimations, clustered_estimations)
