import sys
import time

import pandas as pd
from utilities.ArgumentProcessor import ArgumentProcessor
from utilities.FileFinishFinder import FileFinishFinder
from utilities.FileReader import FileReader
from utilities.FileWriter import FileWriter
from estimators.NaiveModel import NaiveModel
from utilities.MemoryUsage import MemoryUsage
from utilities.Visualization import Visualization
from estimators.StateDiagramModel import State_Diagram_Model
from estimators.Clustering import Clustering
from utilities.Preprocessing import Preprocessing
from utilities.ToDateTime import ToDateTime

if __name__ == "__main__":

    memory_list = []
    def MyThread(memory_list):
        #memory_list.append(os.getpid())
        process = psutil.Process(os.getpid())
        while True:
            time.sleep(10)
            memory_list.append(process.memory_info().rss / 10**6) #Mb
            #print(process.memory_info().rss)  # in bytes

    #print(os.getpid())
    #thread.start()
    #print(memory_list)

    def estimate():

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
        df_Training_original['event time:timestamp'] = pd.to_datetime(
            df_Training_original['event time:timestamp'], dayfirst=True, infer_datetime_format=True)
        print("time _ read training file: " + str("%.0f" % (time.time() - t1)) + "  sec")

        t1 = time.time()
        df_Test_original = a_file_reader.readFile(testAddress)
        df_Test_original['event time:timestamp'] = pd.to_datetime(df_Test_original['event time:timestamp'],
                                                                  dayfirst=True, infer_datetime_format=True)

        print("time _ read test file: " + str("%.0f" % (time.time() - t1)) + "  sec")
        print("memory usage of training DF (in MegaBytes): ",
              MemoryUsage.memory_usage_sum(df_Training_original))
        print("memory usage of test DF (in MegaBytes): ", MemoryUsage.memory_usage_sum(df_Test_original))

        """
        Do the preprocessing if necessary 
        """
        t1 = time.time()

        if ("2019" in trainingAddress):
            pre_processing_instance = Preprocessing()

            df_training_preprocessed = pre_processing_instance.filter(df_Training_original)
            df_test_preproccessed = pre_processing_instance.filter(df_Test_original)

            df_Training_original = df_training_preprocessed
            df_Test_original = df_test_preproccessed

        t2 = time.time()
        print("Time _ preprocessing: " + str("%.0f" % (t2 - t1)) + "  sec")
        """
        Finished preprocessing
        """

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
                df_Training_extra['event concept:name'] + ' ' + df_Training_extra[
                    'event lifecycle:transition']
            df_Test_extra['EventStatus'] = \
                df_Test_extra['event concept:name'] + ' ' + df_Test_extra['event lifecycle:transition']
        else:
            df_Training_extra['EventStatus'] = df_Training_extra['event concept:name']
            df_Test_extra['EventStatus'] = df_Test_extra['event concept:name']

        """
        Train naive estimator
        """
        naive_model = NaiveModel()

        t1 = time.time()

        naive_estimations = naive_model.calc_naive_estimate(df_Training_extra.copy(),
                                                            df_Test_extra.copy(), a_file_finish_finder,
                                                            trainingAddress)

        t2 = time.time()
        print("Time _ calculating naive_estimation: " + str("%.0f" % (t2 - t1)) + "  sec")

        """ 
        Train State Transition estimator 
        """

        t1 = time.time()

        a_State_Diagram_Model = State_Diagram_Model()
        MAX_LENGTH = a_file_finish_finder.get_max_lenght(trainingAddress)
        ST_estimations = a_State_Diagram_Model.calc_state_transition(df_Training_extra.copy(),
                                                                     df_Test_extra.copy(),
                                                                     a_file_finish_finder, MAX_LENGTH)

        print("st: ", ST_estimations[0])

        t2 = time.time()
        print("Time _ calculating ST_estimation: " + str("%.0f" % (t2 - t1)) + "  sec")
        """
        Train cluster estimators
        """
        t1 = time.time()

        df_Training_cluster = df_Training_extra.copy()
        df_Test_cluster = df_Test_extra.copy()
        # Converting to dateTime
        aDateTimeModel = ToDateTime()

        df_Training_cluster = aDateTimeModel.toDateTime(df_Training_cluster)
        df_Test_cluster = aDateTimeModel.toDateTime(df_Test_cluster)

        aClusterModel = Clustering()
        clustersTraining = aClusterModel.clusterData(df_Training_cluster)
        clustersTest = aClusterModel.clusterData(df_Test_cluster)

        naiveClusters = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        clustered_estimations = []
        counter = 0

        # Here we make sure we don't predict for empty months in the testfile
        for i in clustersTest:
            clusterNaiveModel = NaiveModel()
            if not i.empty:
                naiveClusters[counter] = clusterNaiveModel.calc_naive_estimate(clustersTraining[counter],
                                                                               clustersTest[counter],
                                                                               a_file_finish_finder,
                                                                               trainingAddress)
                clustered_estimations.extend(naiveClusters[counter])
            counter += 1

        t2 = time.time()
        print("Time _ calculating Cluster estimation: " + str("%.0f" % (t2 - t1)) + "  sec")

        """
        visualization
        """
        print("visualization started")
        t1 = time.time()

        visualizer = Visualization()

        # Shows the scatter plot for the naive estimator
        plotName = "Naive Prediction"
        naive_graph_scatter = visualizer.create_scatter(naive_estimations, plotName, data_file_name)

        # Shows the scatter plot for the clustered estimator
        plotName = "Clustered Prediction"
        clustered_graph_scatter = visualizer.create_scatter(clustered_estimations, plotName, data_file_name)

        # Shows the scatter plot for the ST estimator
        ST_graph_scatter = visualizer.create_scatter(ST_estimations, "ST Estimator", data_file_name)

        print("Finished visualization of scatter plots")

        # prints the MSE diagrams
        name = "MSE"
        visualizer.create_mse(naive_graph_scatter[0], naive_graph_scatter[1], naive_graph_scatter[2])
        visualizer.create_mse(clustered_graph_scatter[0], clustered_graph_scatter[1],
                              clustered_graph_scatter[2])
        visualizer.create_mse(ST_graph_scatter[0], ST_graph_scatter[1], ST_graph_scatter[2])
        visualizer.finishMSE(name, trainingAddress)
        print("Finished visualization of MSE")

        t2 = time.time()
        print("Time _ calculating Visualization: " + str("%.0f" % (t2 - t1)) + "  sec")

        """
        Writes the estimators to the output file ST SHOULD STILL BE ADDED
        """
        a_file_writer = FileWriter(anEncoding)
        outputFile = a_file_writer.writeFile(outputName, df_Test_original, naive_estimations,
                                             clustered_estimations,
                                             ST_estimations)


    #Threading
    thread_1 = Thread(target=MyThread, args=(memory_list, ))
    thread_1.daemon = True
    thread_1.start()

    estimate()

    print("average RAM usage (RSS)", sum(memory_list) / len(memory_list),
          "  |  Number of times memory usage sampled: ", len(memory_list))



    print("ALL DONE!")
