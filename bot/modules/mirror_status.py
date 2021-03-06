import threading
import time
import psutil, shutil
from telegram import ParseMode
from telegram.ext import CommandHandler
from bot import dispatcher, status_reply_dict, status_reply_dict_lock, download_dict, download_dict_lock, botStartTime
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage, auto_delete_message, sendStatusMessage
from bot.helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from telegram.error import BadRequest
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands

Bot_Photo = "https://telegra.ph/file/c06d92681208824918821.jpg"

def mirror_status(update, context):
    with download_dict_lock:
        if len(download_dict) == 0:
            currentTime = get_readable_time(time.time() - botStartTime)
            total, used, free = shutil.disk_usage('.')
            free = get_readable_file_size(free)
            message = 'No Active Downloads !\n_______________________________'
            message += f"\n<b>CPU:</b> {psutil.cpu_percent()}% | <b>FREE:</b> {free}" \
                       f"\n<b>RAM:</b> {psutil.virtual_memory().percent}% | <b>UPTIME:</b> {currentTime}" 
            update.effective_message.reply_photo(Bot_Photo, message, parse_mode=ParseMode.HTML)
            return
    index = update.effective_chat.id
    with status_reply_dict_lock:
        if index in status_reply_dict.keys():
            deleteMessage(context.bot, status_reply_dict[index])
            del status_reply_dict[index]
    sendStatusMessage(update, context.bot)
    deleteMessage(context.bot, update.message)


mirror_status_handler = CommandHandler(BotCommands.StatusCommand, mirror_status, run_async=True)
dispatcher.add_handler(mirror_status_handler)
