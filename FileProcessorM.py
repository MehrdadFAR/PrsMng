import pandas as pd
from datetime import datetime

class FileProcessorM:
    def __init__(self):
        pass

    # read the file and return a list of DataFrames
    def read_file(self, file_address, an_encoding):
        #print("Started reading file:", str(file_address))
        header_list = []
        isHeader = True
        with open(file_address, 'r', encoding=an_encoding) as f:
            for line in f:
                if isHeader:
                    header_list = [i.replace('"', '') for i in line.strip().split(',')]
                    isHeader = False
                else:
                    temp_dict  = dict(zip(header_list, [i.replace('"', '') for i in line.strip().split(',')]))
                    temp_dict["event time:timestamp"] = datetime.strptime(temp_dict["event time:timestamp"],
                                                                          '%d-%m-%Y %H:%M:%S.%f')
                    yield temp_dict

        #print(" Reading file completed ")



    def write_file(self, name, an_encoding, df_list):
        print("writing to file started.")

        include_header = True
        with open(name, 'w') as f:
            for df in df_list:
                try:
                    df.to_csv(f, header=include_header, encoding=an_encoding, index=False)
                    include_header =  False
                    #print(df['Naive_Predictor'])
                except:
                    print("Exception in writing the file.")

        print("writing to file completed. File name: ", name)


    def pocess(self, x):
        print(x)