import pandas as pd
class FileReader:
    anEncoding = None
    def __init__(self, encoding):
        self.anEncoding = encoding


    def write_file(self, name, testFile, estimators):
        print("writing to file started.")

        #include_header = True
        #with open(name, 'w') as f:
            #for df in df_list:
                #try:
                    #df.to_csv(f, header=include_header, encoding=anEncoding, index=False)
                    include_header = False
                    # print(df['Naive_Predictor'])
                #except:
                    #print("Exception in writing the file.")

        print("writing to file does not actualy happen yet")

        print("writing to file completed. File name: ", name)