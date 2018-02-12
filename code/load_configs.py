import json
from pprint import pprint

configFilePath = 'config.json'
file = open(configFilePath)
data = json.load(file)
file.close()

#pprint(data)

telegram_bot_token = data['telegramBotToken']
logFilePath = data['logging']['logfilePath']
logType = data['logging']['logType']
