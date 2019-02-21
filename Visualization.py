from matplotlib import pyplot as plt
import numpy as np

# Data input:
# List of dictionaries with keys 'timeSpent', 'timeLeft' and 'predLeft'.

class Visualization:

    def create_visualization(self, accDict, remainDict, predictNaiveDict):
        # Transforming dictionaries to lists per key.
        x = []
        y = []
        naivePrediction = []
        #sortAccDict = sorted(accDict)
        #sortRemainDict = sorted(remainDict)
        #sortPredictDict = sorted(predictNaiveDict)

        for key in sorted(accDict.keys()):
            x.append(accDict[key])

        for key in sorted(remainDict.keys()):
            y.append(remainDict[key])

        for key in sorted(predictNaiveDict.keys()):
            naivePrediction.append(predictNaiveDict[key])

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

        mse = []
        for i in range(0, len(y)):
            mse.append((y[i] - naivePrediction[i]) ** 2)

        #print("This is y:")
        #print(mse)
        #print(x)

        # Plot MSE Naive estimator to time spent. Other estimators are commented for now.
        plt.plot(x, mse, color='r', label='Naive Estimator', marker='.')
        # plt.plot(x, meanSquared_est2, color = 'b', label = 'Estimator 2', marker = '.')
        # plt.plot(x, meanSquared_est3, color = 'g', label = 'Estimator 3', marker = '.')
        # plt.plot(x, meanSquared_est4, color = 'y', label = 'Estimator 4', marker = '.')

        plt.legend(loc='upper right')
        plt.ylabel('Mean Squared Error')
        plt.xlabel('Time spent (seconds)')
        plt.title('MSE')
        plt.savefig('MSE.png')  # Saving plot in a .png in current directory
        plt.show()
