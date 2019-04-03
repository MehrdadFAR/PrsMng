class ClusterAttributeFinder:
    def __init__(self):
        self.cluster_attribute = None

    def clusterAttributeDefiner(self, trainingAddress):
        if "Dummy" in trainingAddress:
            self.cluster_attribute = 'something'
        elif "BPI_2012" in trainingAddress:
            self.cluster_attribute = "case AMOUNT_REQ"
            # Amount of money requested for a loan.
        elif "BPI_2017" in trainingAddress:
            self.cluster_attribute = "case RequestedAmount"
        elif "BPI_2018" in trainingAddress:
            self.cluster_attribute = 'case area'
        elif "BPI_2019" in trainingAddress:
            self.cluster_attribute = 'case Document Type'
        elif "italian" in trainingAddress:
            self.cluster_attribute = 'event amount'

        if self.cluster_attribute == None:
            raise Exception("Cluster attribute is not determined")
        return self.cluster_attribute
    #def getClusterAttribute(self):
     #   return self.cluster_attribute
