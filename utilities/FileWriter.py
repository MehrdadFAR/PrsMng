import pandas as pd
class FileWriter:
    anEncoding = None
    def __init__(self, encoding):
        self.anEncoding = encoding


    def writeFile(self, name, testFile, estimators):

        print("creating column")
        testFile['Naive_Predictor'] = 0
        for index, row in testFile.iterrows():
            # Cant figure out how to get the naive estimator per event id so for now hardcoded as 1
            testFile.at[index,'Naive_Predictor'] = 1


        print("writing to file started.")
        try:
            testFile.to_csv(name, index=False, encoding=self.anEncoding)
            print("testfile is put into csv")
        except:
            print("Exception in writing the file.")


        print("writing to file completed. File name: ", name)