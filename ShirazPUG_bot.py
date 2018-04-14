#
# ShirazPUG bot
#
import telepot
from telepot.loop import MessageLoop
import time
from pprint import pprint
allowed_bots = [] # Username
admins = [] # numerical ID <-- set before run !
warning = [] # numerical ID
def main(msg) :
    global warning
    global allowed_bots
    global admins
    content_type, chat_type, chat_id = telepot.glance(msg)
    try :
        if msg['new_chat_member']['is_bot'] and msg['new_chat_member']['username'].lower() not in allowed_bots :
            if msg['new_chat_member']['id'] != msg['from']['id'] :
                bot.sendMessage(chat_id, '[%s](tg://user?id=%d)\n يک بات ناشناس به گروه اضافه کرد!' %(msg['from']['first_name'], msg['from']['id']), 'markdown')
                bot.kickChatMember(chat_id, msg['new_chat_member']['id']) # bot should be admin for this
                if not msg['from']['id'] in warning :
                    warning.append(msg['from']['id'])
                    bot.sendMessage(chat_id, '[%s](tg://user?id=%d)\n يک اخطار گرفت!' %(msg['from']['first_name'], msg['from']['id']), 'markdown')
                else :
                    bot.kickChatMember(chat_id, msg['from']['id']) # bot should be admin for this
            else :
                bot.sendMessage(chat_id, '[%s](tg://user?id=%d)\n به گروه اضافه شد!' %(msg['new_chat_member']['first_name'], msg['new_chat_member']['id']), 'markdown')
                bot.kickChatMember(chat_id, msg['new_chat_member']['id']) # bot should be admin for this
    except :
        pass

    try :
        if msg['from']['id'] in admins and msg['text'].split()[0] == '/addbot' : # example: /addbot @f2fRobot @apkdl_bot ...
            new_bots = msg['text'].split()[1:]
            for new_bot in new_bots :
                new_bot = new_bot.replace('@', '').lower()
                allowed_bots.append(new_bot)
        
        elif msg['from']['id'] in admins and msg['text'].split()[0] == '/rmbot' : # example: /rmbot @f2fRobot @apkdl_bot ...
            rm_bots = msg['text'].split()[1:]
            for rm_bot in rm_bots :
                    rm_bot = rm_bot.replace('@', '').lower()
                    try :
                        allowed_bots.remove(rm_bot)
                    except :
                        pass

        elif msg['from']['id'] in admins and msg['text'] == '/bots' : # show a list of all allowed bots
            es = ''
            for alw_bot in allowed_bots :
                es += '@' + alw_bot + '\n'
            bot.sendMessage(chat_id, 'ليست بات هاي مجاز:\n%s' %(es))
            
    except :
        pass


token = '' # <--  set the token before run
bot = telepot.Bot(token)
MessageLoop(bot, main).run_as_thread()

while 1 :
    time.sleep(10)
