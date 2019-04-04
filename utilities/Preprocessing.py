import pandas as pd
import datetime

class Preprocessing:

    def __init__(self):
        pass

    def filter(self, df):
        start_date = '01-01-2018'
        start_date_object = pd.to_datetime(start_date, dayfirst=True, infer_datetime_format=True)

        end_date = '28-01-2019'
        end_date_object = pd.to_datetime(end_date, dayfirst=True, infer_datetime_format=True)

        mask1 = df['event time:timestamp'] <= start_date_object

        array_cases = df[mask1]['case concept:name'].unique()
        array_events = list(df[df['case concept:name'].isin(array_cases)].index)
        new_df = df.drop(array_events, axis=0)

        new_df2 = new_df[new_df['event time:timestamp'] < end_date]

        return new_df2


