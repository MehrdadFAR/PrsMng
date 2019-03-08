
class ArgumentProcessor:
    anEncoding = 'cp1252'

    def __init__(self):
        pass

    def processArgs(self, arguments):
        if len(arguments) < 4:
            print("Error! Provide three arguments: 'Address_Input' 'Address_Test' 'OutputName.csv' "
                  "...")
            raise SystemExit
        else:
            trainingAddress = arguments[1]  #
            testAddress = arguments[2]  # arguments[2] is the absolute path to the test input file
            outputName = arguments[3]  # name of the output file
            if len(arguments) == 5: #to manually override encoding.
                self.anEncoding = arguments[4]

        if not (outputName.endswith(".csv") or outputName.endswith(".txt")):
            outputName = outputName + ".csv"

        return(trainingAddress, testAddress, outputName, self.anEncoding)