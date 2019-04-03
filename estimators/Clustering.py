import pandas as pd

class Clustering:

    def __init__(self):
        pass
    def clusterData(self, df):
        # Grouping data on first event per case
        grouped = df.groupby('case concept:name').tail(1)

        # Adding month of first event to grouped df
        grouped['month'] = grouped['event time:timestamp'].dt.month

        listmonths = [0,1,2,3,4,5,6,7,8,9,10,11]
        list_per_month = []

        # Creating df per month with all events clustered on their starting month
        for i in listmonths:
            if len(grouped[grouped['month'] == i]) != 0:
                uniqueCases = list(grouped[grouped["month"] == i]['case concept:name'])
                dataMonth = df[df["case concept:name"].isin(uniqueCases)]
                list_per_month.append(pd.DataFrame(dataMonth))
            else: # Empty if no case started in this month
                list_per_month.append(pd.DataFrame({}))


        january = list_per_month[0]
        february = list_per_month[1]
        march = list_per_month[2]
        april = list_per_month[3]
        may = list_per_month[4]
        june = list_per_month[5]
        july = list_per_month[6]
        august = list_per_month[7]
        september = list_per_month[8]
        october = list_per_month[9]
        november = list_per_month[10]
        december = list_per_month[11]

        return january, february, march, april, may, june, july, august, september, october, november, december
