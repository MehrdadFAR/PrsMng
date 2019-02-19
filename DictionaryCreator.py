# new version
import pandas as pd

class DictionaryCreator:
        df_list = None  #????possibility to assign value at objet creation via constructor

        minDict = {}
        accDict = {}
        remainDict = {} # combine with acc dic??
        mainDict = {}

        # createa new dictionary with key eventID and values: Event Time, Event Name Life Cycle THEN add it to mainDict to the list corrspondng to the caseName
        def create_main_dictionary(self, df_list):
            for df in df_list:
                tempDF = pd.DataFrame(df)
                for index, row in tempDF.iterrows():
                    e_ID = row["eventID "]
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

                    if event_time_stamp < min:
                        self.minDict[case_concept_name] = event_time_stamp

            return self.mainDict

        # @pre: create_main_dictionary must have been called once before or else an exception will be thrown.
        def create_min_dictionary(self):
            if self.minDict:
                return self.minDict
            else:
                raise Exception("method create_main_dictionary was not called at least once to create the mindict as side effect")
