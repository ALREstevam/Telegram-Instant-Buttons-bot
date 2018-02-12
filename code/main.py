from Bot import TelegramMyInstantsBot as TmiBot
from pprint import pprint
import load_configs as cnfg
import re
from WebScrapping import MyInstantsWebScrapping as MiWb
import telepot
import traceback
import urllib3
from Logger import lggr

bot = TmiBot(cnfg.telegram_bot_token)
scrap = MiWb()

def convertCountryName(orig):
    if orig == 'pt-br':
        return 'br'
    return orig



def talkFunction(msg):
    chatId = msg['chat']['id']

    try:
        #if the message type is not a text (sticker, image, audio, ...)
        if telepot.glance(msg)[0] != 'text':
            bot.sendText('😉 Please, send-me some text.', chatId)
            return
        data = bot.glanceMsg(msg)

        lggr.logPrint('\n\n>>> [{}]: "{}"'.format(data['fullname'], data['txt']))

        #/start
        if data['txt'] == '/start':
            presentationText = [
                "👋 <b>Hi {}</b>".format(data['first_name']),
                "🔉 Welcome to <b>{}</b> 🎧".format(bot.botName),
                "😄 I am your sound finder tool in myinstants. Enter any terms that I will bring you the top three results. 👍",
                "You can also use:",
                "<code>/top</code> to get the top three results for your language",
                "<code>/top(number)</code> to get the top <code>number</code> results for your language",
                "<code>/top(number) (keyword)</code> to get the top <code>number</code> results when searching for <code>keywords</code>",
                "<i>This page is not official of myinstants.com and all data used is publicly available on their site.</i>"
            ]
            for msg in presentationText:
                bot.sendText(msg, chatId)

        elif '/top' in data['txt']:
            pattern = re.compile(r"/top\s?(\d*)?\s?([A-Za-z À-ú0-9-]*)?")
            matches = pattern.match(data['txt'])
            country = convertCountryName(data['lang'])

            amount = 3

            if not matches.group(1).isdigit() and not matches.group(1) == '':
                bot.sendText("😶 I do not understand how many sounds you want, I'll bring you three.", chatId)
            elif matches.group(1) == '':
                pass
            else:
                amount = int(matches.group(1))


            text = matches.group(2)
            #lggr.logPrint('amount `{}`, text `{}`'.format(amount, text))

            if amount > 50:
                amount = 50

            #/top
            if data['txt'] == '/top':
                bot.sendText('🔍🤔 <b>Searching top three results for region:</b> {}'.format(data['lang']),chatId)
                answ = scrap.getTopByCountry(country)
                bot.sendSounds2(answ, chatId, '', scrap.getUrlForCounty(country))

            #/top <txt>
            elif str(amount) == '' and str(text) != '':
                bot.sendText('🔍🤔 <b>Searching top 5 results for </b>{}'.format(text), chatId)
                answ = scrap.searchByKeyWord(str(text), 5)
                bot.sendSounds2(answ, chatId, text, scrap.getUrlForKeyword(text))

            #/top <n>
            elif str(amount) != '' and str(text) == '':
                bot.sendText('🔍🤔 <b>Searching top {} results</b>'.format(int(amount)), chatId)
                answ = scrap.getTopByCountry(country, int(amount))
                bot.sendSounds2(answ, chatId, '', scrap.getUrlForCounty(country))

            #/top <n> <txt>
            elif str(amount) != '' and str(text) != '':
                bot.sendText('🔍🤔 <b>Searching top {} results for </b>{}'.format(amount, text),
                             chatId)
                answ = scrap.searchByKeyWord(str(text), int(amount))
                bot.sendSounds2(answ, chatId, text, scrap.getUrlForKeyword(text))

            #/top ?
            else:
                bot.sendText('<b>🔍🤔 Searching for:</b> {}'.format(text), chatId)
                bot.sendSounds2(chatId, None, text, scrap.getUrlForKeyword(text))

        #<txt>
        else:
            bot.sendText('🔍🤔 <b>Searching for:</b> {}'.format(data['txt']), chatId)
            answ = scrap.searchByKeyWord(data['txt'])
            bot.sendSounds2(answ, chatId, data['txt'], scrap.getUrlForKeyword(data['txt']))

    except urllib3.exceptions.ReadTimeoutError:
        bot.sendText('😭 Oh no, the connection timed out, please try again.', chatId)
        traceback.print_exc()
    
    except Exception as ex:
        bot.sendText('😭 Oh no, Something went wrong.', chatId)
        traceback.print_exc()






bot.setTalkHandleFunction(talkFunction)
lggr.logPrint('[SERVER IS ONLINE]')
while True:
    cmd = input('<<<: ')

    if cmd.lower() == 'exit':
        exit(0)
    elif cmd == ' ':
        pass
    else:
        lggr.logPrint('>>>: invalid command.')

