from time import gmtime, strftime
import load_configs

class Logger:
    def __init__(self, file='logfile.log', logStatus='both'):
        self.logFile = file
        self.logStatus = logStatus
        with open(self.logFile, 'a', encoding='utf-8') as file:
            file.write('\n[LOG FILE]\n')

    def logPrint(self, strng='', end='\n'):
        if self.logStatus in ['both', 'file']:
            time = strftime("%d-%m-%Y %H:%M:%S", gmtime())
            with open(self.logFile, 'a', encoding='utf-8') as file:
                #file.write('[' + time + ']: ' + strng + end)
                file.write('[{}]:{}\n'.format(time, strng))

        if self.logStatus in ['screen', 'both']:
            print(strng, end=end)



lggr = Logger(load_configs.logFilePath, load_configs.logType)


