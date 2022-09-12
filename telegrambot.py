# import json
# from typing import Union, Any
import config
import datetime
import time
from db import DB

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

TELEGRAM_BOT_TOKEN = config.telegram_bot_token


class WorkTimer:
    async def sendTime(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        db = DB()
        if not db.is_timer_in_progress(update.message.chat.id):
            return False

        now = datetime.datetime.now()
        minutes = now.minute
        print('minute', minutes)

        chat_id = update.effective_chat.id

        if 45 == minutes:
            await context.bot.send_message(chat_id=chat_id, text='--- Скоро перерыв ---')

        if 50 == minutes:
            await context.bot.send_message(chat_id=chat_id, text='--- Перерыв ---')

        if 00 == minutes:
            await context.bot.send_message(chat_id=chat_id, text='--- Продолжаем ---')

        time.sleep(59)
        await self.sendTime(update, context)

    async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        await context.bot.send_message(chat_id=chat_id, text='--- Я тут ---')
        print('chat id', chat_id)
        db = DB()
        db.start_timer(chat_id)
        await self.sendTime(update, context)

    # @staticmethod
    # def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     print('stop')
    #     db = DB()
    #     db.stop_timer(update.message.chat.id)
    #     update.message.reply_text('timer is stopped')


##########


def mb_command_with_params(command_text):
    if command_text[0] != '/':
        return False

    c_list = command_text.split()
    mb_function = c_list[0].replace('/', '')
    mb_function = globals()[mb_function]
    if not callable(mb_function):
        return False

    return mb_function(command_text.replace(c_list[0] + " ", ''))


##########


def bootstrap():
    WorkTimerInstance = WorkTimer()
    application = ApplicationBuilder().token(config.telegram_bot_token).build()
    application.add_handler(CommandHandler('run', WorkTimerInstance.run))
    application.run_polling()
