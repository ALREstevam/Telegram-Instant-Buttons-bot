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
            #self.sendSadMsg(chatId, '<b>Sorry, no results found</b>')
            self.sendSadMsg(chatId, '<b>Desculpe, nenhum resultado encontrado</b>')
            self.sendSticker(chatId, 'CAADBAADzAEAAnMaRAXoufUXMpdyzwI')

    def sendSoundsWithUrl(self, chatId, soundList, searchTerm, searchLink):
        #self.sendLinkMsg(chatId, 'Searching sounds', searchLink)
        self.sendLinkMsg(chatId, 'Procurando sons em', searchLink)
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
            #"👋 <b>Hi {}</b>".format(personName),
            #"🔉 Welcome to <b>{}</b> 🎧".format(self.botName),
            #"😄 I am your sound finder tool in myinstants. Enter any terms that I will bring you the top three results. 👍",
            #"You can also use:",
            #"<code>/top</code> to get the top three results for your language",
            #"<code>/top(number)</code> to get the top <code>number</code> results for your language",
            #"<code>/top(number) (keyword)</code> to get the top <code>number</code> results when searching for <code>keywords</code>",
            #"<i>This page is not official of myinstants.com and all data used is publicly available on their site.</i>",
            #"Project on GitHub: https://github.com/ALREstevam/Telegram-Instant-Buttons-bot"

            "👋 <b>Olá, {}</b>".format(personName),
            "🔉 Bem-vindo(a) ao <b>{}</b> 🎧".format(self.botName),
            "😄 Eu sou sua ferramente para procurar sons no MyInstants, entre quaisquer termos que lhe trarei os três primeiros resultados. 👍",
            "Você também pode usar:",
            "<code>/top</code> para retornar os top 3 resultados para o seu país",
            "<code>/top(number) (keyword)</code> para obter os top <code>number</code> resultados quando procurando por <code>keywords</code>",
            "<code>/help</code> para mostrar a lista completa de comandos",
            "<i>Obs.: esse não é um bot oficial de myinstants.com, todos os dados utilizados são disponibilizados de forma pública no site deles.</i>",
            "Obs.: este projeto está em fase de desenvolvimento e testes, o servidor pode não estar on-line a todo momento.",
            "Página do projeto no GitHub: https://github.com/ALREstevam/Telegram-Instant-Buttons-bot"
        ]

        self.sendMessages(chatId, presentationText)


    def sendHelpMsg(self, chatid):
        msg = [
            "<code>(text)</code> para retornar os top 3 resultados para a pesquisa <code>(text)</code>",
            "<code>/top</code> para retornar os top 5 resultados para o seu país",
            "<code>/top(number)</code> para obter os top <code>number</code> para o seu país",
            "<code>/top(number) (keyword)</code> para obter os top <code>number</code> resultados quando procurando por <code>keywords</code>",
            "<code>/help</code> para exibir essa mensagem",
            "<code>/wakeup</code> para testar se o bot está online",
            "<code>/except</code> para testar o tratamento de excessões.",

            "<i>Obs.: esse não é um bot oficial de myinstants.com, todos os dados utilizados são disponibilizados de forma pública no site deles.</i>",
            "Obs.: este projeto está em fase de desenvolvimento e testes, o servidor pode não estar on-line a todo momento.",
            "Página do projeto no GitHub: https://github.com/ALREstevam/Telegram-Instant-Buttons-bot"
        ]

        self.sendMessages(chatid, msg)




