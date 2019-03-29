__author__ = "Mehrdad Farsadyar"

class Node:
    def __init__(self, name, parent):
        self.name=name
        self.children={} #dictionary with node_name as key and node_object as value
        self.event_members=[] #list of [event_timestamp, case_name] which each represent an event of a that
        # landed in this node.
        self.parent=parent
        self.visitors = []
        self.has_changed_since = True
        self.avg_members_remain_time = None

    def add_event_members(self, child_timestamp, case_name):
        self.event_members.append([child_timestamp, case_name])
        self.has_changed_since = True

    def add_visitors(self, df_index, TrD):
        self.visitors.append(df_index)

        """ 
        # ---
        if df_index == 40622:
            print ('________________________________45299__________________')
            print(self.name)
            print(self.visitors)
            print('memebers', self.event_members)
            for  l in self.event_members:
                print(TrD[l[1]][2])

            print(''---'')
            print(self.is_visiting(df_index))
            print(self.members_avg_remain_time(TrD))
            # ---
        """

    #
    def is_visiting(self, df_index):
        return df_index in self.visitors

    #
    def add_child(self, child_name):
        child_node = self.children.setdefault(child_name, Node(child_name,  self.name))
        return child_node

    #
    """ 
    def add_child(self, child_timestamp, case_name):
        self.add_event_members(child_timestamp, case_name)
    """

    #
    def get_name(self):
        return self.name

    #
    def get_parent(self):
        return self.name

    # if possible makes advance to next node and returns that node, else returns None.
    def visit_next_node(self, name):
        if (name in self.children):
            return self.children[name]
        else:
            return None

    #
    def  members_avg_remain_time(self, TrD):
        #print('inside members  avg', self.event_members)
        if self.has_changed_since == False:
            return self.avg_members_remain_time
        else:
            sum = 0
            count  = 0
            for l in self.event_members:
                event_time =  l[0]
                event_case_finish_time = TrD[l[1]][2]

                if event_case_finish_time != None:
                    sum += max( (event_case_finish_time - event_time).total_seconds(), 0 )
                    count += 1

            self.has_changed_since = False
            if count != 0:
                self.avg_members_remain_time = sum / count
                return self.avg_members_remain_time
            else:
                self.avg_members_remain_time = None
                return self.avg_members_remain_time


"""

"""
class State_Diagram_Model:

    def __init__(self):
        '''
         A list. Meaning of indices:
         0: tst_event_case_concept_name,
         1: tst_event_event_timestamp,
         2: tst_evt_case_start_timestamp,
         3: tst_evt_passed_seconds_since start,
         4: estimate_remaining_seconds
         5: actual_finish_stamp (or None)]
         '''
        self.st_estimations = []

        '''
        training_Dict = {"case concept:name" : [0,1,2,3]}
        where in the list, the indices are: 
        0: returns list of the events in this case. We refer to this as 'eve_list'.
        1:'case_start_timestamp' 
        2:'case_finish_timestamp'
        3: 'a_finish_time' - that is a finish time (in seconds) seen so far, if not known yet then holds None.

        eve_list: list of indices from df_training corresponding to events (seen  so far) of 
        this case. Only  the start and finish events are listed. When a new event of this case is seen, 
        it is added to this list only if it is a start event or it is a finish event. Other 
        middle standing events are of no interest and thus not listed.  
        '''
        self.training_Dict = {}

        self.test_Dict = {}

        self.Root= Node('Root', None)

    def calc_state_transition(self, df_training, df_test, a_file_finish_finder, MAX_LENGTH):
        print("State_Diagram estimator started")
        TsD = self.test_Dict
        TrD = self.training_Dict
        Root = self.Root
        st_estimations = self.st_estimations

        finish_events = a_file_finish_finder.get_finishing_event_list()

        is_end_training = False

        # keep track of the indices from Training DF.
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

            tst_event_id = df_test.loc[index_of_tstEvent, 'eventID ']

            # Time stamp of test-event currently at hand.
            tst_event_timestamp = df_test.loc[index_of_tstEvent, 'event time:timestamp']

            # 'event concept:name' of test-event currently at hand.
            tst_EventStatus = df_test.loc[index_of_tstEvent, "EventStatus"]

            # 'case concept:name' of test-event currently at hand.
            tst_case_concept_name = df_test.loc[index_of_tstEvent, "case concept:name"]

            # retrieve the test-dict and add to it this test-event; initializes the dict if not exist
            # and then add this.
            tst_temp_case_dic = TsD.setdefault(tst_case_concept_name, [[],tst_event_timestamp, None, Root,
                                                                       False])


            #'ev_list': [] --> 0
            #'case_start_timestamp':--> 1
            #'case_finish_timestamp': --> 2
            #'visiting_node':--> 3
            #'is_stuck':--> 4


            #tst_temp_case_dic[0].append(index_of_tstEvent)

            if tst_EventStatus in finish_events:
                tst_temp_case_dic[2] = tst_event_timestamp


            trn_event_timestamp = df_training.loc[index_of_trnEvent, 'event time:timestamp']

            # progress into training file as far as still have not reached a training event
            # with timestamp more than that of the test-event at hand.
            while (not is_end_training) and (trn_event_timestamp < tst_event_timestamp):
                trn_EventStatus = df_training.loc[index_of_trnEvent, "EventStatus"]
                trn_case_concept_name = df_training.loc[index_of_trnEvent, "case concept:name"]

                #print('in while loop - trn_event_concept_name:', trn_event_concept_name, " | " ,
                # trn_event_timestamp)

                # gets the dictionary corresponding to the case of this event, if non-existent then makes it.
                trn_temp_list = TrD.setdefault(trn_case_concept_name, [[], trn_event_timestamp, None, Root,
                                                                       0, [Root]])


                #'ev_list':  --> 0
                #'start_time_stamp': --> 1
                #'finish_time_stamp': --> 2
                #'current_node': --> 3
                #'process_length':--> 4
                #'list of nodes it is at' --> 5


                #trn_temp_list[0].append(index_of_trnEvent)

                if trn_EventStatus in finish_events:
                    trn_temp_list[2] = trn_event_timestamp
                    #on trial
                    for n in trn_temp_list[5]:
                        n.has_changed_since = True


                if trn_temp_list[4] <= MAX_LENGTH:
                    landing_node = trn_temp_list[3].add_child(trn_EventStatus)
                    trn_temp_list[4] += 1
                    trn_temp_list[3] = landing_node
                    #trial
                    trn_temp_list[5].append(landing_node)

                trn_temp_list[3].add_event_members(trn_event_timestamp, trn_case_concept_name)

                # progress to the next training event
                try:
                    index_of_trnEvent = next(df_training_index_iter)
                    trn_event_timestamp = df_training.loc[index_of_trnEvent, 'event time:timestamp']
                except StopIteration:
                    is_end_training = True

                #print(TrD.values())

            # __End of while-loop__

            # assertion: at this point all the training events with timestamp before or equal
            # time_stamp of the test_event are seen.

            # state_diagram is complete. Thus now  update the visiting node of the test case

             #'ev_list': [] --> 0
             #'case_start_timestamp':--> 1
             #'case_finish_timestamp': --> 2
             #'visiting_node':--> 3
             #'is_stuck':--> 4

            if  tst_temp_case_dic[4] == False:
                next_visiting_node = tst_temp_case_dic[3].visit_next_node(tst_EventStatus)

                if(next_visiting_node == None):
                    tst_temp_case_dic[4] = True #is stuck
                else:
                    tst_temp_case_dic[3] = next_visiting_node

            tst_temp_case_dic[3].add_visitors(index_of_tstEvent, TrD) #add this tst event as visitor

            event_estimated_remain_time = tst_temp_case_dic[3].members_avg_remain_time(TrD)

            """  
            if tst_event_id == '15182709391396' :
                print(tst_event_id)
                for l in tst_temp_case_dic[3].event_members:
                    print(l[0], TrD[l[1]][2])
                print(' **************** ')
                print(tst_temp_case_dic[3].members_avg_remain_time())
            """


            #print(event_estimated_remain_time)


             #A list, containing lists which indices are:
             #0: tst_event_case_concept_name,
             #1: tst_event_event_timestamp,
             #2: tst_evt_case_start_timestamp,
             #3: tst_evt_passed_seconds_since_start,
             #4: estimate_remaining_seconds
             #5: actual_finish_stamp (or None)]

            #if  event_estimated_remain_time !=  None:
            tst_case_start_timestamp = tst_temp_case_dic[1]

            tst_evt_passed_seconds_since_start = (tst_event_timestamp -
                                                tst_case_start_timestamp).total_seconds()
            st_estimations.append([tst_case_concept_name, tst_event_timestamp, tst_case_start_timestamp,
                    tst_evt_passed_seconds_since_start, event_estimated_remain_time, None])

            if index_of_tstEvent % 10000 == 0:
                print(index_of_tstEvent)
        # __End of for-loop__

        self.add_actual_finish_timestamp(TsD)


        print('state_transition_estimator_finished.')

        #level = 0
        #self.print_ST(Root,  level, -1)


        return self.st_estimations
        # __End of method__

    #
    def add_actual_finish_timestamp(self, TsD):
        list = self.st_estimations
        for l in list:
            """
            l[0] is the 'event case concept_name'.
            ---
            Retreive the value corresponding to the this key. The result is a list.
            Index 2 of this list is the most update finish time stamp of that case, or holds
            value None if that case did not finish in the test file given. 
            """
            l[5] = TsD[l[0]][2]

    #
    def print_ST(self, node, level, visitor):
        if visitor == -1:
            print("     |"*level, node.name) # , " --> ", node.event_members
            level += 1
            for c in node.children.values():
                self.print_ST(c,level, visitor)
        else:
            if node.is_visiting(visitor):
                print("     |"*level, node.name, "****", node.visitors, "  * * * * ")
                # node.event_members
            else:
                print("     |"*level, node.name) # , " --> ", node.event_members
            level += 1
            for c in node.children.values():
                self.print_ST(c,level, visitor)
