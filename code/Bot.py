import telepot
from telepot.loop import MessageLoop
import WebScrapping as ws
from Logger import lggr

class TelegramMyInstantsBot:
    def __init__(self, botToken):
        self.Ibot = telepot.Bot(botToken)
        try:
            self.Ibot.getMe()
            self.botName = self.Ibot.getMe()['first_name']
            self.botUserName = self.Ibot.getMe()['username']
        except:
            lggr.logPrint('The bot could not be crated.')
            exit(-1)

    def sendText(self, message, chatId, parseMode = 'HTML'):
        self.Ibot.sendChatAction(chatId, 'typing')
        self.Ibot.sendMessage(chatId, message, parse_mode=parseMode)


    def sendSounds(self, soundList, chatId):
        if soundList == None or soundList == [] or not soundList:
            self.sendText('☹ <b>Sorry, no results found</b>', chatId)#😬
        else:
            firstSoundName = soundList[0]['name']
            count = 1

            imgLink = self.imageSearcher(soundList)
            if imgLink != None:
                self.Ibot.sendChatAction(chatId, 'upload_photo')
                self.Ibot.sendPhoto(chatId, imgLink[0], caption='{}'.format(imgLink[1]))

            for item in soundList:
                #lggr.logPrint('[{:30},{}]'.format(item['name'], item['link']))
                #audio = MP3(item['link'])
                #audLen = audio.info.length
                #self.sendText('▶️ {:2} - {}\n🔗 {}'.format(count, item['name'], item['link']), chatId)
                self.Ibot.sendChatAction(chatId, 'upload_audio')
                self.Ibot.sendAudio(chatId, item['link'], title=item['name'], caption='{}\n@{}'.format(item['name'], self.botUserName))
                count += 1

    def sendSounds2(self, soundList, chatId, searchTerm, searchLink):
        self.sendText('Searching sounds at\n🔗: {}'.format(searchLink), chatId)
        return self.sendSounds(soundList, chatId)

    def imageSearcher(self, audios):
        imageScrappers = [ws.GoogleImagesWebScrapping(), ws.DogPileImagesWebScrapping()]

        for audio in audios:
            name = audio['name']
            for imageScr in imageScrappers:
                link = imageScr.searchFirst(name)
                if link != None:
                    return [link, name]
        return None

    def setTalkHandleFunction(self, handle):
        MessageLoop(self.Ibot, handle).run_as_thread()


    def glanceMsg(self, msg):
        return {
            'fullname': msg['from']['first_name'] + ' ' + msg['from']['last_name'],
            'first_name': msg['from']['first_name'],
            'last_name': msg['from']['last_name'],
            'chat_id': msg['chat']['id'],
            'lang': msg['from']['language_code'],
            'txt': msg['text']
        }
