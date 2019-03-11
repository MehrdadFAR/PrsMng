import pandas as pd
class FileWriter:
    anEncoding = None
    def __init__(self, encoding):
        self.anEncoding = encoding


    def writeFile(self, name, testFile, estimators):

        print("creating column")
        testFile['Naive_Predictor'] = 0
        for row in testFile.iterrows():
            # Cant figure out how to get the naive estimator per event id so for now hardcoded as 1
            #row['Naive_Predictor'] = 1
            variable = 1


        print("writing to file started.")
        include_header = True
        with open(name, 'w') as f:
            try:
                testFile.to_csv(f, header=include_header, encoding=anEncoding, index=False)
                print("testfile is put into csv")
            except:
                print("Exception in writing the file.")


        print("writing to file completed. File name: ", name)