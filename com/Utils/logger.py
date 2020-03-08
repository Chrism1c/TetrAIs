import sys
from datetime import datetime


class Logger(object):
    def __init__(self):
        self.dateTimeObj = datetime.now()
        self.terminal = sys.stdout
        fileName = str(
            "LOG_" + str(self.dateTimeObj.year) + "-" + str(self.dateTimeObj.month) + "-" + str(self.dateTimeObj.day)
            + "_" + str(self.dateTimeObj.hour) + "-" + str(self.dateTimeObj.minute) + ".log")
        self.log = open("com/Utils/logs/"+fileName, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


if __name__ == "__main__":
    sys.stdout = Logger()
    print("Hello world 1 !")  # this is should be saved in yourlogfilename.txt
    print("Hello world 2 !")
