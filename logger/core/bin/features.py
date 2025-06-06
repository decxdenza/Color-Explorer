from logger.core.libraries import *

class LogData():

    def __init__(self, data):
        self.time = '{0}:{1}:{2}'.format(datetime.datetime.now().hour if (int(datetime.datetime.now().hour) > 9) else f'0{datetime.datetime.now().hour}', datetime.datetime.now().minute if (int(datetime.datetime.now().minute) > 9) else f'0{datetime.datetime.now().minute}', datetime.datetime.now().second if (int(datetime.datetime.now().second) > 9) else f'0{datetime.datetime.now().second}')
        self.data = data