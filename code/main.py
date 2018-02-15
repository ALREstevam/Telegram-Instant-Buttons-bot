print('STARTING')
from MiBot import MyInsBot as TmiBot
import load_configs as cnfg
from WebScrapping import MyInstantsWebScrapping as MiWb
from pprint import pprint
import re
import telepot
import traceback
import urllib3
import os
from Logger import lgr

bot = TmiBot(cnfg.telegram_bot_token)
scrap = MiWb()

lgr.log('ONLINE')


def convertCountryName(orig):
    if orig == 'pt-br':
        return 'br'
    return orig



def talkFunction(msg):
    chatId = msg['chat']['id']

    try:
        pprint(msg)
        msgType = telepot.glance(msg)[0]
        print(msgType)

        #if the message type is not a text (sticker, image, audio, ...)
        if msgType not in ['text', 'sticker']:
            bot.sendTip(chatId, 'Please, send-me some text.')
            return


        data = bot.glanceMsg(msg)
        print('\n\n>>> [{}]: "{}"'.format(data['fullname'], data['txt']))
        lgr.log('[{}]: "{}"'.format(data['fullname'], data['txt']))


        #/hi /hello /wakeup
        if data['txt'] in ['/hi', '/hello', '/wakeup']:
            bot.sendText(chatId, '👋 Hello there!')

        if data['txt'] == '/except':
            bot.sendText(chatId, 'Testing exeption handling.')
            raise Exception

        # /start
        elif data['txt'] == '/start':
            bot.sendStartMessage(chatId, data['first_name'])


        elif '/top' in data['txt']:
            pattern = re.compile(r"/top\s?(\d*)?\s?([A-Za-z À-ú0-9-]*)?")
            matches = pattern.match(data['txt'])

            if matches is None:
                bot.sendSadMsg(chatId, 'Command <code>/top</code> could not be processed.')
                return

            text = '' if matches.group(2) is None else str(matches.group(2))
            amount = 0 if matches.group(1) is None or not matches.group(1).isnumeric() else int(matches.group(1))

            if amount > 45:
                amount = 45

            if amount < 0:
                amount = 0

            #/top <txt>
            if amount == 0 and text != '':
                bot.sendSearchMsg(chatId, '<b>Searching top 5 results for </b>{}'.format(text))
                answ = scrap.searchByKeyWord(text, 5)
                bot.sendSoundsWithUrl(chatId, answ, text, scrap.getUrlForKeyword(text))

            #/top <n>
            elif amount != 0 and text == '':
                country = convertCountryName(data['lang'])
                bot.sendSearchMsg(chatId, '<b>Searching top {} results</b>'.format(amount))
                answ = scrap.getTopByCountry(country, amount)
                bot.sendSoundsWithUrl(chatId, answ, '', scrap.getUrlForCounty(country))

            #/top <n> <txt>
            elif amount != 0 and text != '':
                bot.sendSearchMsg(chatId, '<b>Searching top {} results for </b>{}'.format(amount, text))
                answ = scrap.searchByKeyWord(text, amount)
                bot.sendSoundsWithUrl(chatId, answ, text, scrap.getUrlForKeyword(text))

            #/top
            #if amount == 0 and text == '':
            else:
                country = convertCountryName(data['lang'])
                bot.sendSearchMsg(chatId, '<b>Searching top three results for region:</b> {}'.format(country))
                answ = scrap.getTopByCountry(country)
                bot.sendSoundsWithUrl(chatId, answ, '', scrap.getUrlForCounty(country))

        #<txt>
        else:
            bot.sendSearchMsg(chatId, '<b>Searching for:</b> {}'.format(data['txt']))
            answ = scrap.searchByKeyWord(data['txt'])
            bot.sendSoundsWithUrl(chatId, answ, data['txt'], scrap.getUrlForKeyword(data['txt']))

    except urllib3.exceptions.ReadTimeoutError:
        bot.sendErrorMsg(chatId, 'Oh no, the connection timed out, please try again.')
        traceback.print_exc()
        bot.sendSticker(chatId, 'CAADBAADGgMAAnMaRAVVEiMGXFjhEQI')
    
    except Exception as ex:
        bot.sendErrorMsg(chatId, 'Oh no, Something went wrong.')
        traceback.print_exc()
        bot.sendSticker(chatId, 'CAADBAAD0wEAAnMaRAVCtzF6SHO6dwI')




bot.setTalkHandleFunction(talkFunction)
print('[SERVER IS ONLINE]')
while True:
    cmd = input('<<<: ')

    if cmd.lower() == 'exit':
        exit(0)
    elif cmd == ' ':
        pass
    else:
        try:
            print(eval(str(cmd)))
        except:
            print('Invalid command')

