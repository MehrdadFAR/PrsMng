import pandas as pd
import numpy as np
class TestClusterer:

    def __init__(self):
        self.test_clusters = None
        self.clusterDataFrame = None
        self.first = None
        self.second = None
        self.third = None
        self.fourth = None
        self.counter = None
        self.bins = None
        self.newDataFrame = None

    def clusterer(self, cluster_attribute, df, trainingClusters, trainingAddress):
        """

        :type df: DataFrame
        """
        if "BPI_2019" in trainingAddress:
            print("busy with cluster one")
            self.one = df[df['case Document Type'] == 'EC Purchase order']
            print("Done with cluster one")
            print("Busy with cluster two")
            self.two = df[df['case Document Type'] == 'Framework order']
            print("Done with cluster two")
            print("Busy with cluster three")
            self.three = df[df['case Document Type'] == 'Standard PO']


            print(self.one.shape[0])
            print(self.two.shape[0])
            print(self.three.shape[0])
            #print(self.four.shape[0])

            return self.one, self.two , self.three#, self.four

        self.clusterDataFrame = pd.DataFrame()
        self.clusterDataFrame['cluster'] = [0, 1, 2, 3, 4, 5, 6, 7]
        self.clusterDataFrame['meanlist'] = [0, 0, 0, 0, 0, 0, 0, 0]

        self.counter = 0
        for i in range(0, len(self.clusterDataFrame['meanlist']) - 1):
            self.clusterDataFrame['meanlist'][i] = trainingClusters[i][cluster_attribute].mean()


        self.newDataFrame = self.clusterDataFrame.sort_values(by = 'meanlist')
        self.newDataFrame= self.newDataFrame.reset_index(drop = True)

        self.bins = [0, 0, 0, 0, 0, 0, 0]
        self.bins[0] = (self.newDataFrame['meanlist'][0] + self.newDataFrame['meanlist'][1])/2
        self.bins[1] = (self.newDataFrame['meanlist'][1] + self.newDataFrame['meanlist'][2])/2
        self.bins[2] = (self.newDataFrame['meanlist'][2] + self.newDataFrame['meanlist'][3])/2
        self.bins[3] = (self.newDataFrame['meanlist'][3] + self.newDataFrame['meanlist'][4])/2
        self.bins[4] = (self.newDataFrame['meanlist'][4] + self.newDataFrame['meanlist'][5])/2
        self.bins[5] = (self.newDataFrame['meanlist'][5] + self.newDataFrame['meanlist'][6])/2
        self.bins[6] = (self.newDataFrame['meanlist'][6] + self.newDataFrame['meanlist'][7])/2

        print("bins:", self.bins)

        df2 = df.copy()
        df2['cluster'] = 0
        print("something: ", self.newDataFrame['cluster'])
        for i in range(0, len(df[cluster_attribute]) - 1):
            if df2[cluster_attribute][i] <= self.bins[0]:
                df2['cluster'][i] = self.newDataFrame['cluster'][0]
            elif self.bins[0] < df2[cluster_attribute][i] <= self.bins[1]:
                df2['cluster'][i] = self.newDataFrame['cluster'][1]
            elif self.bins[1] < df2[cluster_attribute][i] <= self.bins[2]:
                df2['cluster'][i] = self.newDataFrame['cluster'][2]
            elif self.bins[2] < df2[cluster_attribute][i] <= self.bins[3]:
                df2['cluster'][i] = self.newDataFrame['cluster'][3]
            elif self.bins[3] < df2[cluster_attribute][i] <= self.bins[4]:
                df2['cluster'][i] = self.newDataFrame['cluster'][4]
            elif self.bins[4] < df2[cluster_attribute][i] <= self.bins[5]:
                df2['cluster'][i] = self.newDataFrame['cluster'][5]
            elif self.bins[5] < df2[cluster_attribute][i] <= self.bins[6]:
                df2['cluster'][i] = self.newDataFrame['cluster'][6]
            else:
                df2['cluster'][i] = self.newDataFrame['cluster'][7]

        #df['cluster'] = self.newDataFrame['cluster'][0] if df[cluster_attribute] <= self.bins[0]
        #df['cluster'] = self.newDataFrame['cluster'][1] if self.bins[0] < df[cluster_attribute] <= self.bins[1]
        #df['cluster'] = self.newDataFrame['cluster'][2] if self.bins[1] < df[cluster_attribute] <= self.bins[2]
        #df['cluster'] = self.newDataFrame['cluster'][1] if df[cluster_attribute] <= self.bins[3]

        print("finished assigning clusters")
        self.one = df2[df2.cluster == 0]
        self.two = df2[df2.cluster == 1]
        self.three = df2[df2.cluster == 2]
        self.four = df2[df2.cluster == 3]
        self.five = df2[df2.cluster == 4]
        self.six = df2[df2.cluster == 5]
        self.seven = df2[df2.cluster == 6]
        self.eight = df2[df2.cluster == 7]

        print("the unique ones: ", df2['cluster'].unique())
        return self.one, self.two, self.three, self.four, self.five, self.six, self.seven, self.eight
