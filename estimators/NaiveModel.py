class NaiveModel:

    def __init__(self):
        '''
        A list containing lists of the following index contents for every test_event of the test file:
        0: tst_event_case_concept_name,
        1: tst_event_event_timestamp,
        2: tst_evt_case_start_timestamp,
        3: tst_evt_passed_seconds_since start,
        4: estimate_remaining_seconds
        5: actual_finish_stamp (or None)]
        '''
        self.naive_estimations = []

        '''
        training_Dict:
        
       {"case concept:name" : [[], X, Y, Z]}
       where indices have such meaning: 
        0:'ev_list' 
        1:'case_start_timestamp'
        2:'case_finish_timestamp'
        3: 'a_finish_time' - that is a finish time in seconds, if not known yet then holds None

        eve_list: list of indices from df_training corresponding to events (seen  so far) of 
        this case. Only  the start and finish events. When a new event of this case is seen, 
        it is added to this list only if it is a start event or it is a finish event. Othere 
        middle standing events are of no interest and not listed here.  
        X: the time stamp of the firs event of the case. 
        Y: time stamp of the latest-seen finish-event of this case.  If not finish event is seen so
        far, then this holds -1.  
        '''
        self.training_Dict = {}

        '''
        test_Dict:
        {"case concept:name": {'ev_list' : [], 'case_start_timestamp' : X, 'case_finish_timestamp' : Y}}

        eve_list: list of all the the indices from df_test corresponding to events (seen  so far) of 
        this case. 
        X: the time stamp of the firs event of the case. 
        Y: time stamp of the latest-seen finish-event of this case.  If not finish event is seen so
        far, then this holds -1.  
        '''
        self.test_Dict = {}



    '''
    updates the naive_estimations array with dictionaries where in the naive estimation can be 
    found under the key called 'estimate_remaining_seconds'. At moments when there are no 
    finished events are yet seen (i.e recorded in the training_dict) the prediction for such 
    test-event is not done and that event is ignored (meaning at that point in time we do not 
    have enough information to make the prediction). 
    '''
    def predict_naive_estimation(self, tst_event_event_timestamp, tst_event_case_concept_name, TrD, TsD,
                                 index_of_tstEvent):

        tst_evt_case_start_timestamp = TsD[tst_event_case_concept_name][
            'case_start_timestamp']
        tst_evt_passed_seconds = (tst_event_event_timestamp - tst_evt_case_start_timestamp).total_seconds()

        sum_finish_seconds = 0
        count = 0

        for d in TrD.values():
            finish_seconds = d[3]
            if finish_seconds != None:
                sum_finish_seconds += finish_seconds
                count += 1

        # count == 0 means no finished case has encounter in the training file based on which to
        # make the prediction; in such cases, no prediction is  made for the event and the event
        # is accordingly not added to the naive_estimations list.

        if count == 0:
            pass
        else:

            average_finish_seconds= sum_finish_seconds / count
            estimate_remaining_seconds = max(average_finish_seconds - tst_evt_passed_seconds, 0)

            self.naive_estimations.append(
                [tst_event_case_concept_name, tst_event_event_timestamp, tst_evt_case_start_timestamp,
                 tst_evt_passed_seconds, estimate_remaining_seconds, None, index_of_tstEvent])

    #_End of method__


    '''
    calculates the naive estimate and returns naive_estimations list. It calls predict_naive_estimation() 
    and add_actual_finish_timestamp() methods. 
    '''
    def calc_naive_estimate(self, df_training, df_test, a_file_finish_finder, trainingAddress):
        print("Naive estimator started")
        # load here for faster acces s: ?
        TsD = self.test_Dict
        TrD = self.training_Dict

        #load here for faster access: ?
        finish_events = a_file_finish_finder.get_finishing_event_list()

        is_end_training = False
        # index_of_trnEvent keeps track of the indeces from Training DF.
        index_of_trnEvent = None
        # Get an iterator over indices of the training DF
        df_training_index_iter = iter(df_training.index)
        # Initialize index_of_trnEvent.
        try:
            index_of_trnEvent = next(df_training_index_iter)
        except StopIteration:
            is_end_training = True

        # Loop over each event in the TEST DF
        for index_of_tstEvent in df_test.index:

            # Time stamp of test-event currently at hand.
            tst_event_event_timestamp =  df_test.loc[index_of_tstEvent, 'event time:timestamp']
            #'event concept:name' of test-event currently at hand.
            tst_event_event_concept_name = df_test.loc[index_of_tstEvent, "event concept:name"]

            #'case concept:name' of test-event currently at hand.
            tst_event_case_concept_name = df_test.loc[index_of_tstEvent, "case concept:name"]

            #retrive the test-dict and add this test-event; initializes the dict if not exist
            # and then add this.
            TsD.setdefault(tst_event_case_concept_name, {'ev_list' : [],
                    'case_start_timestamp' : tst_event_event_timestamp,
                    'case_finish_timestamp': None})['ev_list'].append(index_of_tstEvent)

            tst_EventStatus = df_test.loc[index_of_tstEvent, 'EventStatus']

            # If this test_event is a finish-event, update the finish timestamp of its case if it is not it is reset to None
            if tst_EventStatus in finish_events:
                TsD[tst_event_case_concept_name]['case_finish_timestamp'] = \
                    tst_event_event_timestamp

            trn_event_event_timestamp = df_training.loc[index_of_trnEvent, 'event time:timestamp']

            # progress into training file as far as still have not reached a training event
            # with timestamp more than that of the test-event at hand.
            while (not is_end_training) and (trn_event_event_timestamp < tst_event_event_timestamp):
                trn_event_event_concept_name = df_training.loc[index_of_trnEvent, "event concept:name"]
                trn_event_case_concept_name = df_training.loc[index_of_trnEvent, "case concept:name"]

                # temp_dict is handle to access the dict corresponding to case_concept_name of this
                # training event in the .
                temp_dict = TrD.setdefault(
                    trn_event_case_concept_name, [[],
                    trn_event_event_timestamp,
                    None, None])

                temp_dict[0].append(index_of_trnEvent)

                trn_EventStatus = df_training.loc[index_of_trnEvent, 'EventStatus']

                if trn_EventStatus in finish_events:
                    temp_dict[2] = trn_event_event_timestamp
                    temp_dict[0].append(index_of_trnEvent)
                    temp_dict[3] = (temp_dict[2] - temp_dict[1]).total_seconds()

                # progress to the next training event
                try:
                    index_of_trnEvent = next(df_training_index_iter)
                    trn_event_event_timestamp = df_training.loc[index_of_trnEvent, 'event time:timestamp']
                except StopIteration:
                    is_end_training = True

            #__End of while-loop__

            # assertion: at this point all the training events with timestamp before or equal
            # time_stamp of the test_event are seen.
            self.predict_naive_estimation(tst_event_event_timestamp, tst_event_case_concept_name, TrD, TsD, index_of_tstEvent)

        #__End of for-loop__

        self.add_actual_finish_timestamp(TsD)

        print("Naive estimator finished.")
        return self.naive_estimations

        # __End of method__


    '''
    Adds the actual finish times to the dcitionaries in the naive_estimations list. If the 
    test-event has a finish time that is not yet seen (not in the test file) then the value will 
    be None.
    '''
    def add_actual_finish_timestamp(self, TsD):
        na_es = self.naive_estimations
        for l in na_es:
            #l[0] is the tst_evt_case_concept_name
            l[5] = TsD[l[0]]['case_finish_timestamp']

