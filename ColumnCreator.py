
class ColumnCreator:
    def __init__(self):
        pass

    def createExtraColumn(self, df_list, test_predictNaive_dictionary):
        print("createExtraColumn initiated")
        for df in df_list:
            print("for df")
            df['Naive_Predictor'] = 0
            for index, row in df.iterrows():
                e_ID = str(row["eventID "])
                row['Naive_Predictor'] = test_predictNaive_dictionary[e_ID]
                #print(e_ID, test_predictNaive_dictionary[e_ID], row['Naive_Predictor'])

        return df_list