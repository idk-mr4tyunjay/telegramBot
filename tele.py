import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pytube import YouTube

# Define the function to handle incoming messages
def download_video(update, context):
    # Get the message text from the user
    message_text = update.message.text

    # Extract the YouTube video URL from the message text
    video_url = message_text.split(' ')[1]

    # Download the video using pytube
    yt = YouTube(video_url)
    video = yt.streams.get_highest_resolution()
    video.download()

    # Send the downloaded video file to the user
    context.bot.send_video(chat_id=update.effective_chat.id, video=open(yt.title+'.mp4', 'rb'))

# Set up the Telegram bot
bot_token = 'YOUR_BOT_TOKEN_HERE'
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher

# Define the command handler for the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! Send me a YouTube video URL and I'll download it for you.")

# Add the command and message handlers to the dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), download_video))

# Start the bot
updater.start_polling()
updater.idle()
