
class ColumnCreator:
    def __init__(self):
        pass

    def createExtraColumn(self, df_list, test_predictNaive_dictionary):
        print("createExtraColumn initiated")
        t = True
        for df in df_list:
            df['Naive_Predictor'] = 0
            for index, row in df.iterrows():
                e_ID = str(row["eventID "])
                df.at[index, 'Naive_Predictor'] =  test_predictNaive_dictionary[e_ID]

        return df_list