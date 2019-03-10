class FileFinishFinder:

    def __init__(self, trainingAddress):
        self.trainingAddress = None
        self.finishing_event_list = None
        self.determine_FinishEvents(trainingAddress)
        print('the finishing event names:', self.get_finishing_event_list())

    def determine_FinishEvents(self, trainingAddress):
        if "dummy" in trainingAddress:
            self.finishing_event_list = ['e3', 'e4']
        elif "BPI_2012" in trainingAddress:
            self.finishing_event_list = ["A_CANCELLED", "A_ACTIVATED", "A_DECLINED", "W_Valideren aanvraag"]
            # not yet checking if the aanvraag is finished !!!!!!!!
        elif "BPI_2017" in trainingAddress:
            self.finishing_event_list = None
        elif "BPI_2018" in trainingAddress:
            self.finishing_event_list = ['case rejected', "case basic payment"]
        elif "italian" in trainingAddress:
            self.finishing_event_list = ["Payment", "Send for Credit Collection"]

        if self.finishing_event_list == None:
            raise Exception("finishing_events are not determined")


    def isFinishEvent(self, eventName):
        if eventName in self.finishing_event_list:
            return True
        else:
            return False

    def get_finishing_event_list(self):
        return self.finishing_event_list