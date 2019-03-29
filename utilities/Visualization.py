from matplotlib import pyplot as plt
import numpy as np
import math

# Data input:
# List of dictionaries with keys 'timeSpent', 'timeLeft' and 'predLeft'.


class Visualization:
    colorCounter = 1

    def create_scatter(self, estimations_list, name, trainingAddress):
        # format estimations list:
        #         0: tst_event_case_concept_name,
        #         1: tst_event_event_timestamp,
        #         2: tst_evt_case_start_timestamp,
        #         3: tst_evt_passed_seconds_since start,
        #         4: estimate_remaining_seconds
        #         5: actual_finish_stamp (or None)]

        # Transforming dictionaries to lists per key.
        x = []  # list of seconds passed since start of case per event
        y = []  # actual remaining time in case
        prediction = []  # predicted remaining time in case

        # additional lists for 2019 file
        x2 = []  # list of seconds passed since start of case per event
        y2 = []  # actual remaining time in case
        prediction2 = []  # predicted remaining time in case

        # The loop which computes the x, y and Prediction values per event
        for i in estimations_list:

            # Take the passed argument and store the needed attributes
            eventTime = i[1]
            startTime = i[2]
            predictTime = i[4] / (3600 * 24)
            endTime = i[5]

            # Compute the time that has passed from the beginning of the case till the current event
            accTime = (eventTime - startTime).total_seconds() / (3600 * 24)

            # Makes sure the event is only visualized if there exists an finishing event
            if endTime != None:
                remainTime = max(0, (endTime - eventTime).total_seconds() / (3600 * 24))

                if "BPI_2019" in trainingAddress:
                    if accTime < 3000:
                        x.append(accTime)
                        y.append(remainTime)
                        prediction.append(predictTime)
                    else:
                        x2.append(accTime)
                        y2.append(remainTime)
                        prediction2.append(predictTime)
                else:
                    x.append(accTime)
                    y.append(remainTime)
                    prediction.append(predictTime)

        nameCounter = 1
        # Computation of first plot: scatter plot of estimated and real value for Estimator.
        plt.scatter(x, y, color='b', label='real remaining time', s=1)
        plt.scatter(x, prediction, color='r', alpha=0.5, label='predicted remaining time', s=1)
        plt.legend(loc='upper right')
        plt.xlabel('Time spent (Days)')
        plt.ylabel('Time left (Days)')
        plt.title(str(name) + ' remaining time')
        # Saving plot in a .png in current directory
        outputName = None
        if "BPI_2012" in trainingAddress:
            outputName = str(name) + str(nameCounter) + '_2012'
        elif "BPI_2017" in trainingAddress:
            outputName = str(name) + str(nameCounter) + '_2017'
        elif "BPI_2018" in trainingAddress:
            outputName = str(name) + str(nameCounter) + '_2018'
        elif "italian" in trainingAddress:
            outputName = str(name) + str(nameCounter) + '_Italian'
        elif "BPI_2019" in trainingAddress:
            outputName = str(name) + str(nameCounter) + '_2019'
        else:
            outputName = str(name) + str(nameCounter) + '_unknown'

        plt.savefig(outputName + '.png', format='png', dpi=1200)

        plt.clf()
        plt.cla()
        plt.close()
        # plt.show()

        if "BPI_2019" in trainingAddress:
            nameCounter = 2
            plt.scatter(x2, y2, color='b', label='real remaining time', s=1)
            plt.scatter(x2, prediction2, color='r', alpha=0.5, label='predicted remaining time', s=1)
            plt.legend(loc='upper right')
            plt.xlabel('Time spent (Days)')
            plt.ylabel('Time left (Days)')
            plt.title(str(name) + ' remaining time')

            outputName = str(name) + str(nameCounter) + '_2019'
            plt.savefig(outputName + '.png', format='png', dpi=1200)

            plt.clf()
            plt.cla()
            plt.close()
            # plt.show()

        if "BPI_2019" in trainingAddress:
            return x, y, prediction, x2, y2, prediction2
        else:
            return x, y, prediction

        # Computing MSE for Naive Estimator
        # meanSquared_naive = self.mse(y, Prediction)

    def create_mse(self, arg1, arg2, Prediction1):

        # The binning method. Makes sure the MSE graph means something visually. Change num_of_bins if more bins are required.
        def binning(x, y, Pred, num_of_bins):
            binsize = (max(x) - min(x)) / (num_of_bins - 1)
            binsX = []
            binsY = []
            binsPred = []

            # Initializes all bins to be empty
            for i in range(0, num_of_bins):
                binsX.append([])
                binsY.append([])
                binsPred.append([])

            # adds all elements in x,y, Pred to their respective bins
            index = 0
            for a in x:
                binsX[int((a - min(x)) / binsize)].append(a)
                binsY[int((a - min(x)) / binsize)].append(y[index])
                binsPred[int((a - min(x)) / binsize)].append(Pred[index])

                index += 1

            # Computes the mean of every x bin
            counter = 0
            for j in binsX:
                binsX[counter] = np.nanmean(j)

                # binsX[counter] = int(binsX[counter])
                counter += 1

            # Computes the mean of every y bin
            counter = 0
            for k in binsY:
                binsY[counter] = np.nanmean(k)

                counter += 1

            # Computes the mean of every naive bin
            counter = 0
            for l in binsPred:
                binsPred[counter] = np.nanmean(l)

                counter += 1

            xList = []
            for n in binsX:
                if not math.isnan(n):
                    xList.append(n)

            yList = []
            for m in binsY:
                if not math.isnan(m):
                    yList.append(m)

            estList = []
            for o in binsPred:
                if not math.isnan(o):
                    estList.append(o)

            return xList, yList, estList

        # Calls the binning function
        tempBins = binning(arg1, arg2, Prediction1, 51)
        # tempBinsCluster = binning(arg3, arg4, Prediction2, 51)

        xBin = tempBins[0]
        yBin = tempBins[1]
        predBin = tempBins[2]


        # Fills the MSE with naive estimator
        mse = []
        for i in range(0, len(yBin)):
            mse.append((yBin[i] - predBin[i]) ** 2)

        colorName = None
        lineName = None

        if self.colorCounter == 1:
            colorName = 'r'
            lineName = 'Naive Estimator'
            self.colorCounter += 1
        elif self.colorCounter == 2:
            colorName = 'g'
            lineName = 'Clustered Estimator'
            self.colorCounter += 1
        elif self.colorCounter == 3:
            colorName = 'b'
            lineName = 'State Transition Estimator'
            self.colorCounter += 1
        else:
            colorName = 'y'
            lineName = 'Estimator'

        plt.plot(xBin, mse, color=colorName, label=lineName, marker='.')


    def finishMSE(self, name, trainingAddress):
        plt.legend(loc='upper right')
        plt.ylabel('Mean Squared Error (Days squared)')
        plt.xlabel('Time spent (Days)')
        plt.title(name)
        if "BPI_2012" in trainingAddress:
            plt.savefig(name + '_2012.png', format='png', dpi=1200)  # Saving plot in a .png in current directory
        elif "BPI_2017" in trainingAddress:
            plt.savefig(name + '_2017.png', format='png', dpi=1200)  # Saving plot in a .png in current directory
        elif "BPI_2018" in trainingAddress:
            plt.savefig(name + '_2018.png', format='png', dpi=1200)  # Saving plot in a .png in current directory
        elif "italian" in trainingAddress:
            plt.savefig(name + '_Italian.png', format='png', dpi=1200)  # Saving plot in a .png in current directory
        elif "BPI_2019" in trainingAddress:
            plt.savefig(name + '_2019.png', format='png', dpi=1200)  # Saving plot in a .png in current directory
        else:
            plt.savefig(name + '_unknown.png', format='png', dpi=1200)  # Saving plot in a .png in current directory
        plt.clf()
        plt.cla()
        plt.close()
