import telepot
from telepot.loop import MessageLoop

bot = telepot.Bot('546564040:AAHeCeSCX_l2pft1tsMF4kCQd1c4iJTvNjg')
print(bot.getUpdates())
#bot.sendMessage('', 'test')


def recebeMsg(msg):
    if msg['text'] == 'exit':
        exit()
    print(msg['text'])
    bot.sendMessage(msg['chat']['id'], 'você digitou: ' + msg['text'])


#bot.message_loop(recebeMsg)
MessageLoop(bot, recebeMsg).run_as_thread()


while True:
    pass
