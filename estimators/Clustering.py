class Clustering:
    cluster_attribute = None
    one = None
    two = None
    three = None
    four = None
    five = None
    def __init__(self):

        def clusterData(self, trainingAddress, df):
            if "dummy" in trainingAddress:
                self.cluster_attribute = None
            elif "BPI_2012" in trainingAddress:
                self.cluster_attribute = ["case AMOUNT_REQ"]
                # Amount of money requested for a loan.
            elif "BPI_2017" in trainingAddress:
                self.cluster_attribute = None
            elif "BPI_2018" in trainingAddress:
                self.cluster_attribute = None
            elif "italian" in trainingAddress:
                self.cluster_attribute = None

            if self.cluster_attribute == None:
                raise Exception("Cluster attribute is not determined")

            clusterdata = pd.DataFrame()
            clusterdata[cluster_attribute] = df[cluster_attribute]

            km = KMeans(n_clusters=5).fit(clusterdata)

            cluster_map = pd.DataFrame()
            cluster_map['data_index'] = clusterdata.index.values
            cluster_map['cluster'] = km.labels_

            df['cluster'] = cluster_map['cluster']

            self.one = df[df.cluster == 0]
            self.two = df[df.cluster == 1]
            self.three = df[df.cluster == 2]
            self.four = df[df.cluster == 3]
            self.five = df[df.cluster == 4]

            return one, two, three, four, five

