from matplotlib import pyplot as plt
#import pandas as pd
import numpy as np
import datetime
import math

# Data input:
# List of dictionaries with keys 'timeSpent', 'timeLeft' and 'predLeft'.

class Visualization:


    def create_visualization(self, estimations_list):
        #format estimations list: event timestamp, estimated remaining time, case start time, case actual end time
        # Transforming dictionaries to lists per key.
        x = []
        y = []
        naivePrediction = []
        #sortAccDict = sorted(accDict)
        #sortRemainDict = sorted(remainDict)
        #sortPredictDict = sorted(predictNaiveDict)

        for i in estimations_list:

            eventTime = i[0]
            predictTime = i[1]
            startTime = i[2]
            endTime = i[3]

            accTime = (eventTime - startTime).total_seconds()

            #remove second line below comment, uncomment first line below this comment when actual code needs to be run.
            #remainTime = (endTime - eventTime).total_seconds()
            remainTime = 76529

            x.append(accTime)
            y.append(remainTime)
            naivePrediction.append(predictTime)

        # Computation of first plot: scatter plot of estimated and real value for Naive Estimator.

        plt.scatter(x, y, color = 'b', label = 'real waiting time', s=1)
        plt.scatter(x, naivePrediction, color = 'r', alpha = 0.5, label = 'predicted waiting time', s=1)
        plt.legend(loc = 'upper right')
        plt.xlabel('Time spent (seconds)')
        plt.ylabel('Time left (seconds)')
        plt.title('Naive prediction waiting time')
        plt.savefig('Naive Estimator.png')  # Saving plot in a .png in current directory
        plt.show()


        # Computing MSE for Naive Estimator
        #meanSquared_naive = self.mse(y, naivePrediction)

        # Computing MSE for Naive Estimator
        # meanSquared_naive = self.mse(y, naivePrediction)
        def binning(x, y, naivePred, num_of_bins):
            binsize = (max(x) - min(x)) / (num_of_bins - 1)
            binsX = []
            binsY = []
            binsNaive = []
            for i in range(0, num_of_bins):
                binsX.append([])
                binsY.append([])
                binsNaive.append([])

            index = 0
            for i in x:
                binsX[int((i - min(x)) / binsize)].append(i)
                binsY[int((i - min(x)) / binsize)].append(y[index])
                binsNaive[int((i - min(x)) / binsize)].append(naivePred[index])

            counter = 0
            for j in binsX:
                binsX[counter] = np.mean(j)

                if math.isnan(binsX[counter]):
                    binsX[counter] = 0

                binsX[counter] = int(binsX[counter])
                counter += 1

            counter = 0
            for k in binsY:
                binsY[counter] = np.mean(k)

                if math.isnan(binsY[counter]):
                    binsY[counter] = 0
                binsY[counter] = int(binsY[counter])
                counter += 1

            counter = 0
            for l in binsNaive:
                binsNaive[counter] = np.mean(l)
                
                if math.isnan(binsNaive[counter]):
                    binsNaive[counter] = 0
                binsNaive[counter] = int(binsNaive[counter])
                counter += 1

            return binsX, binsY, binsNaive


        tempBins = binning(x, y, naivePrediction, 11)

        xBin = tempBins[0]
        yBin = tempBins[1]
        naiveBin = tempBins[2]

        mse = []
        for i in range(0, len(yBin)):
            mse.append((yBin[i] - naiveBin[i]) ** 2)

        # print("This is y:")
        # print(mse)
        # print(x)
        print(xBin)
        print(mse)
        # Plot MSE Naive estimator to time spent. Other estimators are commented for now.
        plt.plot(xBin, mse, color='r', label='Naive Estimator', marker='.')
        # plt.plot(x, meanSquared_est2, color = 'b', label = 'Estimator 2', marker = '.')
        # plt.plot(x, meanSquared_est3, color = 'g', label = 'Estimator 3', marker = '.')
        # plt.plot(x, meanSquared_est4, color = 'y', label = 'Estimator 4', marker = '.')

        plt.legend(loc='upper right')
        plt.ylabel('Mean Squared Error')
        plt.xlabel('Time spent (seconds)')
        plt.title('MSE')
        plt.savefig('MSE.png')  # Saving plot in a .png in current directory

        plt.show()