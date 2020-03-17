import sys
from datetime import datetime


class Logger(object):
    """
    Class useful to save on file all outputs on console as "sys.stdout" wrapper
    It use a TIMESTAMP method to name the new file
    Example: LOG_2020-3-10_20-10.log
    """
    def __init__(self):
        self.dateTimeObj = datetime.now()
        self.terminal = sys.stdout
        fileName = str(
            "LOG_" + str(self.dateTimeObj.year) + "-" + str(self.dateTimeObj.month) + "-" + str(self.dateTimeObj.day)
            + "_" + str(self.dateTimeObj.hour) + "-" + str(self.dateTimeObj.minute) + ".log")
        self.log = open("com/Utils/logs/"+fileName, "a")

    def write(self, message):
        """
        :param message: str message to write
        :return: None
        """
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


if __name__ == "__main__":
    sys.stdout = Logger()
    print("Hello world 1 !")
    print("Hello world 2 !")
