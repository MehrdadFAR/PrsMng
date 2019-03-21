class ClusterAttributeFinder:
    def __init__(self, trainingAddress):
        self.cluster_attribute = None
        self.clusterAttributeDefiner(trainingAddress)
        self.get_a_cluster_attribute_finder()
        print("cluster attributes are: ", self.get_a_cluster_attribute_finder)
    def clusterAttributeDefiner(self, trainingAddress):
        if "dummy" in trainingAddress:
            self.cluster_attribute = None
        elif "BPI_2012" in trainingAddress:
            self.cluster_attribute = "case AMOUNT_REQ"
            # Amount of money requested for a loan.
        elif "BPI_2017" in trainingAddress:
            self.cluster_attribute = "case RequestedAmount"
        elif "BPI_2018" in trainingAddress:
            self.cluster_attribute = 'case area'
        elif "italian" in trainingAddress:
            self.cluster_attribute = 'event amount'

        if self.cluster_attribute == None:
            raise Exception("Cluster attribute is not determined")

    def get_a_cluster_attribute_finder(self):
        return self.cluster_attribute
