import pandas as pd
import sys
class PreprocessingData:

    def __init__(self):
        pass

    # arguments = sys.argv
    # AP = ArgumentProcessor()
    # trainingAddress = AP.processArgs(arguments)
    '''
    Create new column that is the combination of the columns "event concept:name" and "event lifecycle:transition".
    This is to be used by the data set BPI_2012.
    '''
    def createNewColumn2012(self, df):
        df['EventStatus'] = df['event concept:name'] + ' ' + df['event lifecycle:transition']

        return df

    def createNewColumn(self, df):
        df['EventStatus'] = df['event concept:name']

        return df
