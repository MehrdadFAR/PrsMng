class FileFinishFinder:

    def __init__(self, trainingAddress):
        self.trainingAddress = None
        self.finishing_event_list = None
        self.determine_FinishEvents(trainingAddress)
        print('the finishing event names:', self.get_finishing_event_list())

    def determine_FinishEvents(self, trainingAddress):
        if "dummy" in trainingAddress:
            self.finishing_event_list = ['e3', 'e4']
        elif "Dummy_ST" in trainingAddress:
            self.finishing_event_list = ['evA5', 'evA6']
            # not yet checking if the aanvraag is finished !!!!!!!!
        elif "BPI_2012" in trainingAddress:
            self.finishing_event_list = ["A_CANCELLED COMPLETE", "A_CANCELLED SCHEDULE", "A_CANCELLED START", "A_ACTIVATED COMPLETE", "A_ACTIVATED SCHEDULE", "A_ACTIVATED START", "W_Valideren aanvraag COMPLETE"]
        elif "BPI_2017" in trainingAddress:
            self.finishing_event_list = ["W_Call after offers", "W_Validate application", "W_Complete application", "W_Call incomplete files"]
        elif "BPI_2018" in trainingAddress:
            self.finishing_event_list = ['case rejected', "case basic payment"]
        elif "Traffic" in trainingAddress:
            self.finishing_event_list = ["Payment", "Send for Credit Collection"]
        elif "BPI_2019" in trainingAddress:
            self.finishing_event_list = ['Clear Invoice', 'Delete Purchase Order Item']


        if self.finishing_event_list == None:
            raise Exception("finishing_events are not determined")


    def isFinishEvent(self, eventName):
        if eventName in self.finishing_event_list:
            return True
        else:
            return False

    def get_finishing_event_list(self):
        return self.finishing_event_list

    def get_max_lenght(self, trainingAddress):
        if "dummy" in trainingAddress:
            return None
        elif "Dummy_ST" in trainingAddress:
            return 7
        elif "BPI_2012" in trainingAddress:
            return 11
        elif "BPI_2017" in trainingAddress:
            return 35
        elif "BPI_2018" in trainingAddress:
            return 52
        elif "Traffic" in trainingAddress:
            return 5
        elif "BPI_2019" in trainingAddress:
            return 6
