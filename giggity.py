from telegram.ext import Updater,CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from NOTES_DB import *

# NEW_NOTE, ADD_NOTE, SHOW_ALL, ADD_TO_NOTE, SHOW_NOTE, RM_FROM_NOTE, RM_NOTE, RM_USER

import os
PORT = int(os.environ.get('PORT', 50000))
TOKEN = 'token'


import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


########################### messages


START_MSG = 'oh Hi\!\nGreetings from *Giggity Giggity Bot*\n_This is a personal note keeping bot\nmade by @M\_A\_A\_L\_I\_K_\n'
START_MSG+= 'Press /help for more'

HELP_MSG = '*Here are the various available commands & their syntax \-\>*\n\n'
HELP_MSG+= '/start : _to start the bot_\n\n'
HELP_MSG+= '/help : _display this msg_\n\n'
HELP_MSG+= '/new\_note <name\> : _creates a new note_\n'
HELP_MSG+= '_Name can min 3 chars & max 20 chars_\n\n'
HELP_MSG+= '/show\_all : _shows all current notes_\n\n'
HELP_MSG+='/append\_note <name\> <msg\> : _appends msg to note_\n'
HELP_MSG+='_Max size of msg \= 100 chars_\n\n'
HELP_MSG+='/show\_note <name\> : _show the data in the note with *index*_\n\n'
HELP_MSG+='/rm\_from\_note <name\> <index\> : _removes msg at index from note_\n'
HELP_MSG+='_eg \- /rm\_from\_note maalik 3_\n\n'
HELP_MSG+='/rm\_note <name\> : _deletes the note_\n\n'
HELP_MSG+='/rm\_user : _deletes all user data_\n\n'

ERR_MSG = '*Error*\n_Invalid syntax_,\nLook at /help for more'


########################### functions


def start(update, context):
    
    print(update)

    if(len(context.args)) != 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ERR_MSG,parse_mode=ParseMode.MARKDOWN_V2)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=START_MSG,parse_mode=ParseMode.MARKDOWN_V2)


def help(update, context):

    if(len(context.args)) != 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ERR_MSG,parse_mode=ParseMode.MARKDOWN_V2)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=HELP_MSG,parse_mode=ParseMode.MARKDOWN_V2)
    

def new_note(update, context):
    
    if len(context.args) != 1 or len(context.args[0]) < 3 or len(context.args[0]) > 20:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ERR_MSG,parse_mode=ParseMode.MARKDOWN_V2)
    
    else:
        if NEW_NOTE(name=context.args[0],user_ID=str(update.effective_chat.id)):
            context.bot.send_message(chat_id=update.effective_chat.id, text='New note created :\n'+context.args[0])
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Error\nnote '+context.args[0]+' already exist')


def show_all(update,context):
    
    if len(context.args) != 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ERR_MSG, parse_mode=ParseMode.MARKDOWN_V2)
    else:
        notes = SHOW_ALL(user_ID=str(update.effective_chat.id))

        if notes == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text='_No notes for current user_', parse_mode=ParseMode.MARKDOWN_V2)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Current notes :\n\n'+notes)
    
    
def append_note(update,context):
    
    if len(context.args) < 2 or len(context.args) > 103:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ERR_MSG, parse_mode=ParseMode.MARKDOWN_V2)
    
    else:
        print(context.args)
        if APPEND_NOTE(name=context.args[0],user_ID=str(update.effective_chat.id),data=context.args):
            context.bot.send_message(chat_id=update.effective_chat.id, text='_Data added to note successfully\!_',parse_mode=ParseMode.MARKDOWN_V2)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='*Error*\n_This note does not exist_',parse_mode=ParseMode.MARKDOWN_V2)


def show_note(update,context):
    
    if len(context.args) != 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ERR_MSG, parse_mode=ParseMode.MARKDOWN_V2)
    
    else:
        note = SHOW_NOTE(name=context.args[0],user_ID=str(update.effective_chat.id))
        
        if note == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text='*Error*\nNote _not found_', parse_mode=ParseMode.MARKDOWN_V2)
        elif note == 1:
            context.bot.send_message(chat_id=update.effective_chat.id, text='_This note is empty_', parse_mode=ParseMode.MARKDOWN_V2)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=note)
    

def rm_from_note(update,context):
    
    if len(context.args) != 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ERR_MSG, parse_mode=ParseMode.MARKDOWN_V2)    
    else:
        try:
            int(context.args[1])
            output = RM_FROM_NOTE(name=context.args[0],user_ID=str(update.effective_chat.id),note_ID=int(context.args[1]))

            if output == 0:
                context.bot.send_message(chat_id=update.effective_chat.id, text='*Error*\nNote _not found_',parse_mode=ParseMode.MARKDOWN_V2)
            elif output == 'empty_note':
                context.bot.send_message(chat_id=update.effective_chat.id, text='*Error*\n_this note is empty_',parse_mode=ParseMode.MARKDOWN_V2)
            elif output == 'key_not_found':
                context.bot.send_message(chat_id=update.effective_chat.id, text='*Error*\n_invalid key, check again_',parse_mode=ParseMode.MARKDOWN_V2)
            elif output == 'done':
                context.bot.send_message(chat_id=update.effective_chat.id, text='_Item removed successfully_',parse_mode=ParseMode.MARKDOWN_V2)
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text=ERR_MSG, parse_mode=ParseMode.MARKDOWN_V2)    
 

def rm_note(update,context):
    
    if len(context.args) != 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ERR_MSG, parse_mode=ParseMode.MARKDOWN_V2)
        
    else:
        if RM_NOTE(name=context.args[0],user_ID=str(update.effective_chat.id)):
            context.bot.send_message(chat_id=update.effective_chat.id, text='_Note deleted successfully_',parse_mode=ParseMode.MARKDOWN_V2)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='*Error*\n_Note not found_',parse_mode=ParseMode.MARKDOWN_V2)


def rm_user(update,context):
    
    if len(context.args) != 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ERR_MSG, parse_mode=ParseMode.MARKDOWN_V2)
    
    else:
        if  RM_USER(user_ID=str(update.effective_chat.id)):
            context.bot.send_message(chat_id=update.effective_chat.id, text='*_All data has been removed successfully_*',parse_mode=ParseMode.MARKDOWN_V2)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='*Error*\n_Data does not exist for this user_',parse_mode=ParseMode.MARKDOWN_V2)


def main():
    
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    ######################### add handlers & dispatchers

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler('help', help))

    dispatcher.add_handler(CommandHandler('new_note',new_note))

    dispatcher.add_handler(CommandHandler('show_all',show_all))

    dispatcher.add_handler(CommandHandler('append_note',append_note))

    dispatcher.add_handler(CommandHandler('show_note',show_note))

    dispatcher.add_handler(CommandHandler('rm_from_note',rm_from_note))

    dispatcher.add_handler(CommandHandler('rm_note',rm_note)) 

    dispatcher.add_handler(CommandHandler('rm_user',rm_user))


    ######### start bot

    # updater.start_polling()
    
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook('URL' + TOKEN)
    
    updater.idle()    


if __name__ == '__main__':
    main()
