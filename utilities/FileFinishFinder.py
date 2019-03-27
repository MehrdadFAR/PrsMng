class FileFinishFinder:

    def __init__(self, trainingAddress):
        self.trainingAddress = None
        self.finishing_event_list = None
        self.determine_FinishEvents(trainingAddress)
        print('the finishing event names:', self.get_finishing_event_list())

    def determine_FinishEvents(self, trainingAddress):
        if "Dummy" in trainingAddress:
            self.finishing_event_list = ['Klaar']
        elif "BPI_2012" in trainingAddress:
            self.finishing_event_list = ["A_CANCELLED COMPLETE", "A_CANCELLED SCHEDULE", "A_CANCELLED START", "A_ACTIVATED COMPLETE", "A_ACTIVATED SCHEDULE", "A_ACTIVATED START", "W_Valideren aanvraag COMPLETE"]
            # not yet checking if the aanvraag is finished !!!!!!!!
        elif "BPI_2017" in trainingAddress:
            self.finishing_event_list = ["W_Call after offers", "W_Validate application", "A_Pending", "W_Call incomplete files"]
        elif "BPI_2018" in trainingAddress:
            self.finishing_event_list = ['case rejected', "case basic payment"]
        elif "italian" in trainingAddress:
            self.finishing_event_list = ["Payment", "Send for Credit Collection"]
        elif "BPI_2019" in trainingAddress:
            self.finishing_event_list = ['clear_invoice', 'delete_purchase']

        if self.finishing_event_list == None:
            raise Exception("finishing_events are not determined")


    def isFinishEvent(self, eventName):
        if eventName in self.finishing_event_list:
            return True
        else:
            return False

    def get_finishing_event_list(self):
        return self.finishing_event_list