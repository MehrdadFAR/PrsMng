from matplotlib import pyplot as plt
# import pandas as pd
import numpy as np
import datetime
import math


# Data input:
# List of dictionaries with keys 'timeSpent', 'timeLeft' and 'predLeft'.

class Visualization:

    def create_scatter(self, estimations_list, name):
        # format estimations list:
        #         0: tst_event_case_concept_name,
        #         1: tst_event_event_timestamp,
        #         2: tst_evt_case_start_timestamp,
        #         3: tst_evt_passed_seconds_since start,
        #         4: estimate_remaining_seconds
        #         5: actual_finish_stamp (or None)]

        # Transforming dictionaries to lists per key.
        x = [] # list of seconds passed since start of case per event
        y = [] # actual remaining time in case
        prediction = [] #predicted remaining time in case

        #The loop which computes the x, y and Prediction values per event
        for i in estimations_list:

            #Take the passed argument and store the needed attributes
            eventTime = i[1]
            startTime = i[2]
            predictTime = i[4]/3600
            endTime = i[5]

            #Compute the time that has passed from the beginning of the case till the current event
            accTime = (eventTime - startTime).total_seconds()/3600

            #Makes sure the event is only visualized if there exists an finishing event
            if endTime != None:
                remainTime = max(0,(endTime - eventTime).total_seconds()/3600)

                x.append(accTime)
                y.append(remainTime)
                prediction.append(predictTime)

        # Computation of first plot: scatter plot of estimated and real value for Estimator.
        plt.scatter(x, y, color='b', label='real remaining time', s=1)
        plt.scatter(x, prediction, color='r', alpha=0.5, label='predicted remaining time', s=1)
        plt.legend(loc='upper right')
        plt.xlabel('Time spent (hours)')
        plt.ylabel('Time left (hours)')
        plt.title(str(name) + ' remaining time')

        outputName = str(name) + '.png'
        plt.savefig(outputName)  # Saving plot in a .png in current directory
        plt.show()
        return x, y, prediction


        # Computing MSE for Naive Estimator
        # meanSquared_naive = self.mse(y, Prediction)

    def create_mse(self, arg1, arg2, Prediction1, arg3, arg4, Prediction2):

        #The binning method. Makes sure the MSE graph means something visualy. Change num_of_bins if more bins are required.
        def binning(x, y, Pred, num_of_bins):
            binsize = (max(x) - min(x)) / (num_of_bins - 1)
            binsX = []
            binsY = []
            binsNaive = []

            #Initializes all bins to be empty
            for i in range(0, num_of_bins):
                binsX.append([])
                binsY.append([])
                binsNaive.append([])


            #adds all elements in x,y, Pred to their respective bins
            index = 0
            for a in x:
                binsX[int((a - min(x)) / binsize)].append(a)
                binsY[int((a - min(x)) / binsize)].append(y[index])
                binsNaive[int((a - min(x)) / binsize)].append(Pred[index])

                index += 1

            #Computes the mean of every x bin
            counter = 0
            for j in binsX:
                binsX[counter] = np.mean(j)

                if math.isnan(binsX[counter]):
                    binsX[counter] = 0

                #binsX[counter] = int(binsX[counter])
                counter += 1

            # Computes the mean of every y bin
            counter = 0
            for k in binsY:
                binsY[counter] = np.mean(k)

                if math.isnan(binsY[counter]):
                    binsY[counter] = 0
                #binsY[counter] = int(binsY[counter])
                counter += 1

            # Computes the mean of every naive bin
            counter = 0
            for l in binsNaive:
                binsNaive[counter] = np.mean(l)

                if math.isnan(binsNaive[counter]):
                    binsNaive[counter] = 0
                #binsNaive[counter] = int(binsNaive[counter])
                counter += 1

            return binsX, binsY, binsNaive

        #Calls the binning function
        tempBinsNaive = binning(arg1, arg2, Prediction1, 21)
        tempBinsCluster = binning(arg3, arg4, Prediction2, 21)

        xBinNaive = tempBinsNaive[0]
        yBinNaive = tempBinsNaive[1]
        naiveBin = tempBinsNaive[2]


        xBinCluster = tempBinsCluster[0]
        yBinCluster = tempBinsCluster[1]
        clusterBin = tempBinsCluster[2]


        #Fills the MSE with naive estimator
        mseNaive = []
        for i in range(0, len(yBinNaive)):
            mseNaive.append((yBinNaive[i] - naiveBin[i]) ** 2)

        #Fills the MSE with the clustered estimator

        mseCluster = []
        for i in range(0, len(yBinCluster)):
            mseCluster.append((yBinCluster[i] - clusterBin[i]) ** 2)


        #For testing purpose printing, should be removed later
        print("xbin ", xBinNaive)
        print("Mse ", mseNaive)


        # Plot MSE Naive estimator to time spent. Other estimators are commented for now.
        plt.plot(xBinNaive, mseNaive, color='r', label='Naive Estimator', marker='.')
        plt.plot(xBinCluster, mseCluster, color='g', label='Clustered Estimator', marker='.')

        plt.legend(loc='upper right')
        plt.ylabel('Mean Squared Error (hours squared)')
        plt.xlabel('Time spent (hours)')
        plt.title('MSE')
        plt.savefig('MSE.png')  # Saving plot in a .png in current directory

        plt.show()