class FileFinishFinder:

    def __init__(self, trainingAddress):
        self.trainingAddress = None
        self.finishing_event_list = None
        self.data_file_name = None
        self.determine_FinishEvents(trainingAddress)
        print('the finishing event names:', self.get_finishing_event_list())

    def determine_FinishEvents(self, trainingAddress):
        if "dummy" in trainingAddress:
            self.finishing_event_list = ['e3', 'e4']
            self.data_file_name = "dummy"
        elif "Dummy"in trainingAddress:
            self.finishing_event_list = ['Klaar']
            self.data_file_name = "Dummy"
        elif "Dummy_ST" in trainingAddress:
            self.finishing_event_list = ['evA5', 'evA6']
            self.data_file_name = "dummy_ST"
        elif "BPI_2012" in trainingAddress:
            self.finishing_event_list = ["A_CANCELLED COMPLETE", "A_CANCELLED SCHEDULE", "A_CANCELLED START",
                                         "A_ACTIVATED COMPLETE", "A_ACTIVATED SCHEDULE", "A_ACTIVATED START",
                                         "W_Valideren aanvraag COMPLETE"]
            self.data_file_name = "BPI_2012"
        elif "BPI_2017" in trainingAddress:
            self.finishing_event_list = None
            self.data_file_name = "BPI_2017"
        elif "BPI_2018" in trainingAddress:
            self.finishing_event_list = ['case rejected', "case basic payment"]
            self.data_file_name = "BPI_2018"
        elif "Traffic" in trainingAddress:
            self.finishing_event_list = ["Payment", "Send for Credit Collection"]
            self.data_file_name = "Traffic"
        elif "BPI_2019" in trainingAddress:
            self.finishing_event_list = ['Clear Invoice', 'Delete Purchase Order Item']
            self.data_file_name = "BPI_2019"

        if self.finishing_event_list == None:
            self.data_file_name = trainingAddress
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
        elif "Dummy" in trainingAddress:
            return None
        elif "Dummy_ST" in trainingAddress:
            return 7
        elif "BPI_2012" in trainingAddress:
            return 20
        elif "BPI_2017" in trainingAddress:
            return 35
        elif "BPI_2018" in trainingAddress:
            return 52
        elif "Traffic" in trainingAddress:
            return 5
        elif "BPI_2019" in trainingAddress:
            return 6

    def get_data_file_name(self):
        return self.data_file_name



