import pandas as pd
import datetime

class Preprocessing:

    def __init__(self):
        pass

    def filter(self, df):
        start_date = '01-01-2018'
        end_date = '31-12-2019'
        start_date_object = pd.to_datetime(start_date, dayfirst=True, infer_datetime_format=True)
        end_date_object = pd.to_datetime(end_date, dayfirst=True, infer_datetime_format=True)

        mask = (df["event time:timestamp"] >= start_date_object) & (df["event time:timestamp"] <= end_date_object)
        new_df = df.loc[mask]

        return new_df
