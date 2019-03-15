from matplotlib import pyplot as plt
# import pandas as pd
import numpy as np
import datetime
import math


# Data input:
# List of dictionaries with keys 'timeSpent', 'timeLeft' and 'predLeft'.

class Visualization:

    def create_visualization(self, estimations_list):
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
        naivePrediction = [] #predicted remaining time in case

        #The loop which computes the x, y and naivePrediction values per event
        for i in estimations_list:

            #Take the passed argument and store the needed attributes
            eventTime = i[1]
            startTime = i[2]
            predictTime = i[4]
            endTime = i[5]

            #Compute the time that has passed from the beginning of the case till the current event
            accTime = (eventTime - startTime).total_seconds()

            #Makes sure the event is only visualized if there exists an finishing event
            if endTime != None:
                remainTime = (endTime - eventTime).total_seconds()

                x.append(accTime)
                y.append(remainTime)
                naivePrediction.append(predictTime)


        # Computation of first plot: scatter plot of estimated and real value for Naive Estimator.
        plt.scatter(x, y, color='b', label='real waiting time', s=1)
        plt.scatter(x, naivePrediction, color='r', alpha=0.5, label='predicted waiting time', s=1)
        plt.legend(loc='upper right')
        plt.xlabel('Time spent (seconds)')
        plt.ylabel('Time left (seconds)')
        plt.title('Naive prediction waiting time')
        plt.savefig('Naive Estimator.png')  # Saving plot in a .png in current directory
        plt.show()


        # Computing MSE for Naive Estimator
        # meanSquared_naive = self.mse(y, naivePrediction)

        #The binning method. Makes sure the MSE graph means something visualy. Change num_of_bins if more bins are required.
        def binning(x, y, naivePred, num_of_bins):
            binsize = (max(x) - min(x)) / (num_of_bins - 1)
            binsX = []
            binsY = []
            binsNaive = []

            #Initializes all bins to be empty
            for i in range(0, num_of_bins):
                binsX.append([])
                binsY.append([])
                binsNaive.append([])


            #adds all elements in x,y, naivePred to their respective bins
            index = 0
            for i in x:
                binsX[int((i - min(x)) / binsize)].append(i)
                binsY[int((i - min(x)) / binsize)].append(y[index])
                binsNaive[int((i - min(x)) / binsize)].append(naivePred[index])

                index += 1


            #Computes the mean of every x bin
            counter = 0
            for j in binsX:
                binsX[counter] = np.mean(j)

                if math.isnan(binsX[counter]):
                    binsX[counter] = 0

                binsX[counter] = int(binsX[counter])
                counter += 1

            # Computes the mean of every y bin
            counter = 0
            for k in binsY:
                binsY[counter] = np.mean(k)

                if math.isnan(binsY[counter]):
                    binsY[counter] = 0
                binsY[counter] = int(binsY[counter])
                counter += 1

            # Computes the mean of every naive bin
            counter = 0
            for l in binsNaive:
                binsNaive[counter] = np.mean(l)

                if math.isnan(binsNaive[counter]):
                    binsNaive[counter] = 0
                binsNaive[counter] = int(binsNaive[counter])
                counter += 1

            return binsX, binsY, binsNaive

        #Calls the binning function
        tempBins = binning(x, y, naivePrediction, 11)

        xBin = tempBins[0]
        yBin = tempBins[1]
        naiveBin = tempBins[2]

        #Fills the MSE
        mse = []
        for i in range(0, len(yBin)):
            mse.append((yBin[i] - naiveBin[i]) ** 2)


        #print(xBin)
        #print(mse)


        # Plot MSE Naive estimator to time spent. Other estimators are commented for now.
        plt.plot(xBin, mse, color='r', label='Naive Estimator', marker='.')

        plt.legend(loc='upper right')
        plt.ylabel('Mean Squared Error')
        plt.xlabel('Time spent (seconds)')
        plt.title('MSE')
        plt.savefig('MSE.png')  # Saving plot in a .png in current directory

        plt.show()