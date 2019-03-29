import pandas as pd

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
        if "Dummy" in trainingAddress:
            self.cluster_attribute = ["something"]
        elif "BPI_2012" in trainingAddress:
            self.cluster_attribute = ["case AMOUNT_REQ"]
            # Amount of money requested for a loan.
        elif "BPI_2017" in trainingAddress:
            self.cluster_attribute = ["case RequestedAmount"]
        elif "BPI_2018" in trainingAddress:
            self.cluster_attribute = ['case area']
        elif "italian" in trainingAddress:
            self.cluster_attribute = ['event amount']
        elif "BPI_2019" in trainingAddress:
            self.cluster_attribute = ['event Cumulative net worth (EUR)']

        if self.cluster_attribute is None:
            raise Exception("Cluster attribute is not determined")

        mask1 = df['event Cumulative net worth (EUR)'] <= 1.360000e+02

        mask2 = (df['event Cumulative net worth (EUR)'] > 1.360000e+02) & (
                    df['event Cumulative net worth (EUR)'] <= 4.990000e+02)

        mask3 = (df['event Cumulative net worth (EUR)'] > 4.990000e+02) & (
                    df['event Cumulative net worth (EUR)'] <= 2.166000e+03)

        mask4 = df['event Cumulative net worth (EUR)'] > 2.166000e+03

        df_group_1 = df[mask1]

        df_group_2 = df[mask2]

        df_group_3 = df[mask3]

        df_group_4 = df[mask4]

        self.one =  df[mask1]
        self.two =  df[mask2]
        self.three =  df[mask3]
        self.four = df[mask4]
        '''
        self.five = df[df.cluster == 4]
        self.six = df[df.cluster == 0]
        self.seven = df[df.cluster == 1]
        self.eight = df[df.cluster == 2]
        self.nine = df[df.cluster == 3]
        self.ten = df[df.cluster == 4]
        '''
        #print(self.one.shape[0])
        #print(self.two.shape[0])
        #print(self.three.shape[0])
        #print(self.four.shape[0])
        '''
        print(self.five.shape[0])
        print(self.six.shape[0])
        print(self.seven.shape[0])
        print(self.eight.shape[0])
        print(self.nine.shape[0])
        print(self.ten.shape[0])
        '''

        return self.one, self.two , self.three, self.four#, self.five, self.six, self.seven, self.eight, self.nine, self.ten