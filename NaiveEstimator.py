import pandas as pd
import numpy as np

class NaiveEstimator:

    def train_naive_estimator(self, minDict, maxDict):
        list_finish_time = []
        for key,   max_timestamp in maxDict.items():
            min_timestamp = minDict[key]
            list_finish_time.append((max_timestamp - min_timestamp).total_seconds())

            naive_estimator = sum(list_finish_time) / len(list_finish_time)

        return naive_estimator

