# Import bot token to access bot via telegram http api
from asyncore import dispatcher
import json
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

TOKEN = None
SONG_LIST = []
with open("config.json") as file:
    TOKEN = json.load(file)
    file.close()

# Create a function called start
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text= TOKEN.get("WelcomeText"))
    print("id: ", update.effective_chat.id)

def echo(update: Update, context: CallbackContext):
    for title in SONG_LIST:
        for tag in title.get("tags"):
            if tag.strip().upper() == update.message.text.strip().upper():
                context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=TOKEN.get("LIB_CHAT_ID"), message_id=title.get("id"))
    
def audio(update: Update, context: CallbackContext):
    global SONG_LIST, TOKEN
    if TOKEN.get("LIB_CHAT_ID") == 100:
        TOKEN["LIB_CHAT_ID"] = update.effective_chat.id
        with open("config.json", 'w') as file:
            file.write(json.dumps(TOKEN))
        print("Id for LIB channel updated to: ", update.effective_chat.id)
    if update.effective_chat.id != TOKEN.get("LIB_CHAT_ID"): 
        return
    print(update.channel_post)
    tags = update.channel_post.caption.split("::")
    SONG_LIST.append({"tags": tags, "id": update.channel_post.message_id})
    with open("SONGLIST.json", 'w') as file:
        file.write(json.dumps(SONG_LIST))
        file.close()
    with open("SONGLIST.json", 'r') as file:
        SONG_LIST = json.load(file)
        file.close() 












if __name__ == '__main__':
    # Creates an updater object (used to fetch new updates from telegram bot)
    updater = Updater(token=TOKEN.get("TOKEN"), use_context=True)

    # create variable for easy access to the dispatcher from the update object created
    dispatcher = updater.dispatcher
    
    # Set up logging for easy debugging
    import logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # Open file for recording songs name, tags and ids
    with open("SONGLIST.json", 'r') as file:
        SONG_LIST = json.load(file)
        file.close()
    
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