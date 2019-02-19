import pandas as pd

class InputProcessor:
    def __init__(self):
        pass

    # read the file and return a list of DataFrames
    def read_file(self, training_address, an_encoding):
        print("Reading file started.")
        chunk_size = 100000
        a_list = []
        try:
            for chunk in pd.read_csv(training_address, chunksize=chunk_size, encoding=an_encoding, low_memory=False, delimiter=','):
                a_list.append(chunk)
        except:
            print("Exception in reading the file.")
        print("Reading file completed. Number of DataFrames: ", len(a_list) )
        return a_list