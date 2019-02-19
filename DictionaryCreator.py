# new version
import pandas as pd
import numpy as np

class DictionaryCreator:
        df_list = None  #????possibility to assign value at objet creation via constructor

        minDict = {}
        maxDict = {}
        accDict = {}
        remainDict = {} # combine with acc dic??
        mainDict = {}
        predictNaiveDict = {}

        # createa new dictionary with key eventID and values: Event Time, Event Name Life Cycle THEN add it to mainDict to the list corrspondng to the caseName
        def create_main_dictionary(self, df_list):
            for df in df_list:
                tempDF = pd.DataFrame(df)
                for index, row in tempDF.iterrows():
                    e_ID = str(row["eventID "])
                    case_concept_name = str([row["case concept:name"]])

                    tempDict = {e_ID: {"event concept:name": row["event concept:name"],
                                                "event lifecycle:transition": row["event lifecycle:transition"],
                                                "event time:timestamp": row["event time:timestamp"]
                                       }
                                }

                    self.mainDict.setdefault(case_concept_name, []).append(tempDict)

                    # create min dictionary as side effect to prevent looping twice.
                    event_time_stamp = pd.to_datetime(str(tempDict[e_ID][ "event time:timestamp"]), format='%d-%m-%Y %H:%M:%S.%f')
                    #print(event_time_stamp)
                    min = self.minDict.setdefault(case_concept_name, event_time_stamp)
                    max = self.maxDict.setdefault(case_concept_name, event_time_stamp)

                    if event_time_stamp < min:
                        self.minDict[case_concept_name] = event_time_stamp

                    if event_time_stamp > max:
                        self.maxDict[case_concept_name] = event_time_stamp

            return self.mainDict

        # @pre: create_main_dictionary must have been called once before or else an exception will be thrown.
        def create_min_dictionary(self):
            if self.minDict:
                return self.minDict
            else:
                raise Exception("method create_main_dictionary was not called at least once to create the mindict as side effect")

        def create_max_dictionary(self):
            if self.maxDict:
                return self.maxDict
            else:
                raise Exception("method create_main_dictionary was not called at least once to create the maxdict as side effect")

        def create_acc_remain_predict_dictionary(self, df_list, naive_estimator):
            for df in df_list:
                tempDF = pd.DataFrame(df)
                for index, row in tempDF.iterrows():
                    e_ID = row["eventID "]
                    case_concept_name = str([row["case concept:name"]])
                    time = pd.to_datetime(str(row["event time:timestamp"]), format='%d-%m-%Y %H:%M:%S.%f')
                    minValue = self.minDict[case_concept_name]
                    accValue = (time - minValue) / np.timedelta64(1, 's')
                    self.accDict[e_ID] = accValue
                    predictValue = max(0, (naive_estimator - accValue))
                    self.predictNaiveDict[e_ID] =  predictValue
                    #
                    maxValue = self.maxDict[case_concept_name]
                    self.remainDict[e_ID] = (maxValue - time) / np.timedelta64(1, 's')

            return self.accDict, self.predictNaiveDict, self.remainDict
