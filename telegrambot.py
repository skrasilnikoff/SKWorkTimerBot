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

        time.sleep(58)
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


job_minute = None


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi! Use /set <seconds> to set a timer")


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    chat_id = '' # get from DB

    now = datetime.datetime.now()
    minutes = now.minute
    print('minute', minutes)

    if 39 == minutes:
        await context.bot.send_message(chat_id, text='--- Скоро перерыв ---')

    if 40 == minutes:
        await context.bot.send_message(chat_id, text='--- Перерыв ---')

    if 41 == minutes:
        await context.bot.send_message(chat_id, text='--- Продолжаем ---')


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        # due = float(context.args[0])
        # if due < 0:
        #     await update.effective_message.reply_text("Sorry we can not go back to future!")
        #     return

        job_removed = remove_job_if_exists(str(chat_id), context)
        # context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)
        context.job_queue.run_repeating(alarm, interval=60, first=0)

        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)


##########


def bootstrap():
    WorkTimerInstance = WorkTimer()
    application = ApplicationBuilder().token(config.telegram_bot_token).build()

    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))

    application.add_handler(CommandHandler('run', WorkTimerInstance.run))
    application.run_polling()
