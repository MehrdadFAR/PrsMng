import pandas as pd
from sklearn.cluster import KMeans

class Clustering:
    cluster_attribute = None
    one = None
    two = None
    three = None
    four = None
    five = None
    def __init__(self):
        pass

    def clusterData(self, trainingAddress, df):
        if "dummy" in trainingAddress:
            self.cluster_attribute = None
        elif "BPI_2012" in trainingAddress:
            self.cluster_attribute = ["case AMOUNT_REQ"]
            # Amount of money requested for a loan.
        elif "BPI_2017" in trainingAddress:
            self.cluster_attribute = ["case RequestedAmount"]
        elif "BPI_2018" in trainingAddress:
            self.cluster_attribute = ['case area']
        elif "italian" in trainingAddress:
            self.cluster_attribute = ['event amount']

        if self.cluster_attribute == None:
            raise Exception("Cluster attribute is not determined")

        clusterdata = pd.DataFrame()
        clusterdata[self.cluster_attribute] = df[self.cluster_attribute]

        km = KMeans(n_clusters=2, random_state = 3425).fit(clusterdata)

        cluster_map = pd.DataFrame()
        cluster_map['data_index'] = clusterdata.index.values
        cluster_map['cluster'] = km.labels_

        df['cluster'] = cluster_map['cluster']

        self.one = df[df.cluster == 0]
        self.two = df[df.cluster == 1]
        self.three = df[df.cluster == 2]
        self.four = df[df.cluster == 3]
        '''
        self.five = df[df.cluster == 4]
        self.six = df[df.cluster == 0]
        self.seven = df[df.cluster == 1]
        self.eight = df[df.cluster == 2]
        self.nine = df[df.cluster == 3]
        self.ten = df[df.cluster == 4]
        '''
        print(self.one.shape[0])
        print(self.two.shape[0])
        print(self.three.shape[0])
        print(self.four.shape[0])
        '''
        print(self.five.shape[0])
        print(self.six.shape[0])
        print(self.seven.shape[0])
        print(self.eight.shape[0])
        print(self.nine.shape[0])
        print(self.ten.shape[0])'''
        return self.one, self.two , self.three, self.four#, self.five, self.six, self.seven, self.eight, self.nine, self.ten

