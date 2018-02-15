import telepot

import WebScrapping as ws
from GeneralBot import GeneralTelegramBotWrapper


class MyInsBot(GeneralTelegramBotWrapper):
    def __init__(self, botToken):
        super().__init__(botToken)
        self.emojis = {'search': '🔍🤔', 'happy': '🙂', 'sad': '☹', 'tip': '😉', 'error': '❌😭'}

    def sendSounds(self, chatId, soundList):
        if not soundList == None and not soundList == [] and soundList:
            imgLink = self.imageSearcher(soundList)
            if imgLink != None:
                self.sendPic(chatId, imgLink[0], '{}'.format(imgLink[1]))
            for item in soundList:
                self.sendAudio(chatId, item['link'], title=item['name'], caption='{}\n@{}'.format(item['name'], self.botUserName))
        else:
            self.sendSadMsg(chatId, '<b>Sorry, no results found</b>')
            self.sendSticker(chatId, 'CAADBAADzAEAAnMaRAXoufUXMpdyzwI')

    def sendSoundsWithUrl(self, chatId, soundList, searchTerm, searchLink):
        self.sendLinkMsg(chatId, 'Searching sounds', searchLink)
        return self.sendSounds(chatId, soundList)

    def imageSearcher(self, audios):
        imageScrappers = [ws.GoogleImagesWebScrapping(), ws.DogPileImagesWebScrapping()]
        for audio in audios:
            name = audio['name']
            for imageScr in imageScrappers:
                link = imageScr.searchFirst(name)
                if link != None:
                    return [link, name]
        return None


    def sendSearchMsg(self, chatid, msg):
        return self.sendText(chatid, '{} {}'.format(self.emojis['search'], msg))

    def sendErrorMsg(self, chatid, msg):
        return self.sendText(chatid, '{} {} '.format(self.emojis['error'], msg))

    def sendLinkMsg(self, chatid, msg, url):
        return self.sendText(chatid, '{}\n🔗: {}'.format(msg, url))

    def sendSadMsg(self, chatid, msg):
        return self.sendText(chatid, '{} {}'.format(self.emojis['sad'], msg))

    def sendHappyMsg(self, chatid, msg):
        return self.sendText(chatid, '{} {}'.format(self.emojis['happy'], msg))

    def sendTip(self, chatid, msg):
        return self.sendText(chatid, '{} {}'.format(self.emojis['tip'], msg))

    def sendStartMessage(self, chatId, personName):
        presentationText = [
            "👋 <b>Hi {}</b>".format(personName),
            "🔉 Welcome to <b>{}</b> 🎧".format(self.botName),
            "😄 I am your sound finder tool in myinstants. Enter any terms that I will bring you the top three results. 👍",
            "You can also use:",
            "<code>/top</code> to get the top three results for your language",
            "<code>/top(number)</code> to get the top <code>number</code> results for your language",
            "<code>/top(number) (keyword)</code> to get the top <code>number</code> results when searching for <code>keywords</code>",
            "<i>This page is not official of myinstants.com and all data used is publicly available on their site.</i>",
            "Project on GitHub: https://github.com/ALREstevam/Telegram-Instant-Buttons-bot"
        ]
        for msg in presentationText:
            self.sendText(chatId, msg)




