# Import bot token to access bot via telegram http api
from asyncore import dispatcher
from tokenize import Token
import TOKEN
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


# Create a function called start
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text= TOKEN.welcomeText)
    print("id: ", update.effective_chat.id)

def echo(update: Update, context: CallbackContext):
    for title in TOKEN.SONG_LIST:
        if title[0] == update.message.text:
            context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=TOKEN.LIB_CHAT_ID, message_id=title[1])
    
def audio(update: Update, context: CallbackContext):
    if TOKEN.LIB_CHAT_ID == None:
        TOKEN.LIB_CHAT_ID = update.effective_chat.id
        print("Id for LIB channel: ", update.effective_chat.id)
    if update.effective_chat.id != TOKEN.LIB_CHAT_ID: 
        return
    print(update.channel_post)
    TOKEN.SONG_LIST.append([update.channel_post.caption, update.channel_post.message_id])













if __name__ == '__main__':
    # Creates an updater object (used to fetch new updates from telegram bot)
    updater = Updater(token=TOKEN.token, use_context=True)

    # create variable for easy access to the dispatcher from the update object created
    dispatcher = updater.dispatcher
    
    # Set up logging for easy debugging
    import logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # Create a handler to deal with /start command
    # Connect the handler to the start function created
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    
    echo_handler = MessageHandler(Filters.audio & Filters.chat_type.channel, audio)
    dispatcher.add_handler(echo_handler)

    # start polling (loop until break with ctrl+c)
    updater.start_polling()
    
    updater.idle()