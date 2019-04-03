import pandas as pd


class FileWriter:
    anEncoding = None

    def __init__(self, encoding):
        self.anEncoding = encoding

    def writeFile(self, name, df_test, estimatorsNaive, estimatorsClustered):

        print("creating column naive + filling naive")
        df_test['Naive_Predictor'] = "NaN"
        for l in  estimatorsNaive:
            index = l[6]
            estimation = l[4]
            df_test.at[index, 'Naive_Predictor'] = round(estimation)

        print("creating column cluster + filling cluster")
        df_test['Clustered_Predictor'] = "NaN"
        for l in  estimatorsClustered:
            index = l[6]
            estimation = l[4]
            df_test.at[index, 'Clustered_Predictor'] = round(estimation)

        '''
        print("creating column ST + filling cluster")
        df_test['ST_Predictor'] = "NaN"
        for l in estimatorST:
            index = l[6]
            estimation = l[4]
            df_test.at[index, 'ST_Predictor'] = round(estimation)
        '''
        print("writing to file started.")
        try:
            df_test.to_csv(name, index=False, encoding=self.anEncoding)
            print("testfile is put into csv")
        except:
            print("Exception in writing the file.")
            print("writing to file completed. File name: ", name)
