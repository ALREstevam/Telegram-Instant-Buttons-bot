# MyInstants Telegram Bot

This is a bot made for Telegram using the telepot library.
It uses WebScrapping to retrieve mp3 sounds from www.myinstants.com and sends them to the user.

## Commands

* `<keywords>` gets the first three results when searching for `<keywords>`
* `/top` gets the first three results when accessing the index page for the user's language
* `/top<number>` gets the first `<number>` results when accessing index for the user's language
* `/top <keywords>` gets the fist three when searching for `<keywords>`
* `/top<number> <keywords>` gets the first `<number>` results when searching for `<keywords>`

## Configuration

The bot's configuration it's made by changing the values in the file `config.json`

	{
	  "telegramBotToken": "API-TOKEN-HERE",
	  "logging": {
	    "logfilePath": "logfile.log",
	    "logType": "both"
	  }
	}


* `telegramBotToken`: the bot token given by bot father
* `logging > logfilePath`: the path to the log file
* `logging > logType`: the type of logging, could be:
	* `screen`: everything sent to `logPrint` will be printed on the current terminal
	* `file`: everything sent to `logPrint` will be appended to the log file
	* `both`:  everything sent to `logPrint` will be printed on the current terminal and appended to the log file