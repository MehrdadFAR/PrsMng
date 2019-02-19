import pandas as pd
import numpy as np

class NaiveEstimatorTraining:
    def train_naive_estimator(self, inData):
        timestamp = inData.columns.get_loc("event time:timestamp")
        inData[inData.columns[timestamp]] = pd.to_datetime(inData[inData.columns[timestamp]],
                                                           format='%d-%m-%Y %H:%M:%S.%f')

        # Grouping cases by start and end time
        start_end_log = inData.groupby('case concept:name')['event time:timestamp'].apply(list)

        timeDelta = []

        for i in start_end_log:
            # print(i)
            first = i[0]
            last = max(i)
            timeDelta.append(last - first)

        estimation = pd.DataFrame(timeDelta, columns=['timedelta'])
        meanEstimation = np.mean(estimation['timedelta'])

        secEstimation = meanEstimation / np.timedelta64(1, 's')

        return secEstimation