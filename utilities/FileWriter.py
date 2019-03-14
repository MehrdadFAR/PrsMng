import pandas as pd
class FileWriter:
    anEncoding = None
    def __init__(self, encoding):
        self.anEncoding = encoding


    def writeFile(self, name, df_test, estimators):

        print("creating column")
        df_test['Naive_Predictor'] = "NaN"
        for l in  estimators:
            index = l[6]
            estimation = l[4]
            df_test.at[index, 'Naive_Predictor'] = estimation

        print("writing to file started.")
        try:
            df_test.to_csv(name, index=False, encoding=self.anEncoding)
            print("testfile is put into csv")
        except:
            print("Exception in writing the file.")

        print("writing to file completed. File name: ", name)
