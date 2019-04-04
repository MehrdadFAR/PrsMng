from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math
import warnings

class Visualization:
    colorCounter = 1

    def create_scatter(self, estimations_list, estimator_name, data_file_name):
        print(data_file_name)
        # format estimations list:
        #         0: tst_event_case_concept_name,
        #         1: tst_event_event_timestamp,
        #         2: tst_evt_case_start_timestamp,
        #         3: tst_evt_passed_seconds_since start,
        #         4: estimate_remaining_seconds
        #         5: actual_finish_stamp (or None)]

        start_to_current_time_list = []  # list of seconds passed since start of case per event ;previusly :x
        current_to_finish_time_list = []  # actual remaining time in case ;previously y
        estimated_current_to_finish_time_list = []  # predicted remaining time in case; previously predicted

        start_to_current_time_list_2 = []  # list of seconds passed since start of case per event
        current_to_finish_time_list_2 = []  # actual remaining time in case
        estimated_current_to_finish_time_list_2 = []  # predicted remaining time in case

        count_missed_estimations = 0
        count_all_estimations = 0

        for i in estimations_list:
            count_all_estimations +=1

            if i[4] == None:
                count_missed_estimations += 1
            else:
                current_timestamp = i[1]
                start_timestamp = i[2]
                estimated_remain_time = i[4] / (3600 * 24)
                finish_timestamp = i[5]

                start_to_current_time = (current_timestamp - start_timestamp).total_seconds() / (3600 * 24)

                # Makes sure the event is only visualized if there exists a finishing event
                if finish_timestamp != None:
                    current_to_finish_time = max(0, (finish_timestamp - current_timestamp).total_seconds() / (
                            3600 * 24))

                    start_to_current_time_list.append(start_to_current_time)
                    current_to_finish_time_list.append(current_to_finish_time)
                    estimated_current_to_finish_time_list.append(estimated_remain_time)

        ratio_missed = count_missed_estimations / count_all_estimations

        # plotting
        title = estimator_name + ' Remaining Time    |  ratio of estimations missed = ' + str(round(ratio_missed,2))

        output_name = estimator_name + ' ' + data_file_name

        self.make_plot(start_to_current_time_list, current_to_finish_time_list, estimated_current_to_finish_time_list,
                       title, output_name)

        #return values
        return start_to_current_time_list, current_to_finish_time_list, estimated_current_to_finish_time_list


    """
    """
    def make_plot(self, x, y_real, y_estimated, title, output_name):

        font = {'size': 20}

        plt.rc('font', **font)

        plt.scatter(x, y_real, color='b', label='Real Remaining Time', s=1)

        plt.scatter(x, y_estimated, color='r', alpha=0.5, label='Predicted Remaining Time', s=1)

        blue_patch = mpatches.Patch(color='blue', label='Real Remaining Time')
        red_patch = mpatches.Patch(color='red', label='Predicted Remaining Time')
        plt.legend(handles=[blue_patch, red_patch], loc='upper right', fontsize=14)

        plt.xlabel('Time Spent (Days)', fontsize=26)
        plt.ylabel('Time Left (Days)', fontsize=26)
        plt.title(title)

        figure = plt.gcf()  # get current figure
        figure.set_size_inches(16, 12)

        plt.savefig(output_name + '.png', dpi=1200)

        #plt.show()

        plt.clf()
        plt.cla()
        plt.close()


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
                '''
                binsX[int((a - min(x)) / binsize)].append(a)
                binsY[int((a - min(x)) / binsize)].append(y[index])
                binsPred[int((a - min(x)) / binsize)].append(Pred[index])
                '''

                binsX[0].append(a)
                binsY[0].append(y[index])
                binsPred[0].append(Pred[index])


                index += 1

            # Computes the mean of every x bin
            counter = 0
            for j in binsX:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    binsX[counter] = np.nanmean(j)

                # binsX[counter] = int(binsX[counter])
                counter += 1

            # Computes the mean of every y bin
            counter = 0
            for k in binsY:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    binsY[counter] = np.nanmean(k)

                counter += 1

            # Computes the mean of every naive bin
            counter = 0
            for l in binsPred:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
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

        print("MSE: ", mse)

        plt.plot(xBin, mse, color=colorName, label=lineName, marker='.')


    def finishMSE(self, name, trainingAddress):
        font = {'size': 20}

        plt.rc('font', **font)

        plt.legend(loc='upper right', fontsize=14)
        plt.ylabel('Mean Squared Error (Days squared)', fontsize=20)
        plt.xlabel('Time spent (Days)', fontsize=20)
        plt.title(name)

        figure = plt.gcf()  # get current figure
        figure.set_size_inches(16, 12)

        #plt.show()

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
        elif "Sample" in trainingAddress:
            plt.savefig(name + '_Sample.png', format='png', dpi=1200)  # Saving plot in a .png in current directory
        else:
            plt.savefig(name + '_unknown.png', format='png', dpi=1200)  # Saving plot in a .png in current directory





        plt.clf()
        plt.cla()
        plt.close()

