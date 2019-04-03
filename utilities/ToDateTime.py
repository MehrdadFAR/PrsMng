import pandas as pd
import numpy as np
from datetime import datetime, time
class ToDateTime:

    def __init__(self):
        self.data = None

    def toDateTime(self, df):
        x = 'event time:timestamp'
        self.data = df.copy()
        self.data[x] = pd.to_datetime(df[x], format='%d-%m-%Y %H:%M:%S.%f')
        return self.data
