from time import gmtime, strftime
import load_configs

class Logger:
    def __init__(self, file='logfile.log'):
        self.logFile = file

    def log(self, strng=''):
        time = strftime("%d-%m-%Y %H:%M:%S", gmtime())
        with open(self.logFile, 'a', encoding='utf-8') as file:
            file.write('[{}]:{}\n'.format(time, strng))


lgr = Logger(load_configs.logFilePath)


