import telepot
from telepot.loop import MessageLoop
import traceback

bot = telepot.Bot('')
print(bot.getUpdates())
#bot.sendMessage('', 'test')

def recebeMsg(msg):

    try:
        if telepot.glance(msg)[0] == 'text':
            print('<<< ' + msg['text'])
            answ = str(eval(str(msg['text'])))
            print('>>> ' + answ)
            bot.sendMessage(msg['chat']['id'],'>>> ' + answ)
        else:
            bot.sendMessage(msg['chat']['id'], '>>>')
    except:
        bot.sendMessage(msg['chat']['id'], traceback.format_exc())




#bot.message_loop(recebeMsg)
MessageLoop(bot, recebeMsg).run_as_thread()


while True:
    pass
