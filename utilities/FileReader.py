import pandas as pd
class FileReader:
    anEncoding = None
    def __init__(self, encoding):
        self.anEncoding = encoding

    def readFile(self, address):
        return pd.read_csv(address, encoding=self.anEncoding, low_memory=False)