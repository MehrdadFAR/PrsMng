import pandas as pd
class MemoryUsage:
    #in MegaBytes
    def memory_usage_sum(df):
        return (round(df.memory_usage(deep=True).sum() / 1024 ** 2, 2))

    def memory_usage_detailed(df):
        df.memory_usage(deep=True) / 1024 ** 2