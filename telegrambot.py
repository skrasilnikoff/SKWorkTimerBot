# import json
# from typing import Union, Any
import random

import config
import datetime
from db import DB

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = config.telegram_bot_token


# class WorkTimer:

# async def sendTime(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#     db = DB()
#     if not db.is_timer_in_progress(update.message.chat.id):
#         return False
#
#     now = datetime.datetime.now()
#     minutes = now.minute
#     print('minute', minutes)
#
#     chat_id = update.effective_chat.id
#
#     if 45 == minutes:
#         await context.bot.send_message(chat_id=chat_id, text='--- Скоро перерыв ---')
#
#     if 50 == minutes:
#         await context.bot.send_message(chat_id=chat_id, text='--- Перерыв ---')
#
#     if 00 == minutes:
#         await context.bot.send_message(chat_id=chat_id, text='--- Продолжаем ---')
#
#     time.sleep(58)
#     await self.sendTime(update, context)

# async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     await context.bot.send_message(chat_id=chat_id, text='--- Я тут ---')
#     print('chat id', chat_id)
#     db = DB()
#     db.start_timer(chat_id)
#     await self.sendTime(update, context)

# @staticmethod
# def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print('stop')
#     db = DB()
#     db.stop_timer(update.message.chat.id)
#     update.message.reply_text('timer is stopped')


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Sends explanation on how to use the bot."""
#     await update.message.reply_text("Hi! Use /set <seconds> to set a timer")


async def alarm(context: CallbackContext):
    """Send the alarm message."""
    db = DB()
    chats_ids = db.get_all_active_subscriptions()
    now = datetime.datetime.now()
    minutes = now.minute

    print('minute', minutes)

    for chat_id in chats_ids:

        print('chat_id[0]', chat_id[0])

        chat_id = chat_id[0]

        ### how to send sticker
        # sticker = 'CAACAgIAAxkBAAEYQDdjKYJdUuAF0zuWWFGs5_zM8cWOVAAC1QADgwRdAiDbTvDRO-lVKQQ'
        # await context.bot.send_sticker(chat_id=chat_id, sticker=sticker)

        if 45 == minutes:
            messages = [
                'Перерыв через 5 минут',
                'Скоро отдохнем)',
                'Вот вот перерыв!'
            ]
            message = random.choice(messages)
            await context.bot.send_message(chat_id, text=message)

        if 50 == minutes:
            messages = [
                'Давайте прервемся )',
                'Перерыв)',
                'Го отдохнем',
                'Время отдохнуть немножечко'
            ]
            message = random.choice(messages)
            await context.bot.send_message(chat_id, text=message)

        if 00 == minutes:
            messages = [
                'Пора работать! =)',
                'Время сделать немного денюжек)',
                'Ну что, погнали!',
                'Не расслабляться!'
            ]
            message = random.choice(messages)
            await context.bot.send_message(chat_id, text=message)


# async def set_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Add a job to the queue."""
#     chat_id = update.effective_message.chat_id
#     try:
#         # args[0] should contain the time for the timer in seconds
#         # due = float(context.args[0])
#         # if due < 0:
#         #     await update.effective_message.reply_text("Sorry we can not go back to future!")
#         #     return
#
#         job_removed = remove_job_if_exists(str(chat_id), context)
#         # context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)
#         context.job_queue.run_repeating(alarm, interval=60, first=0)
#
#         text = "Timer successfully set!"
#         if job_removed:
#             text += " Old one was removed."
#         await update.effective_message.reply_text(text)
#
#     except (IndexError, ValueError):
#         await update.effective_message.reply_text("Usage: /set <seconds>")

async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    db = DB()
    db.start_timer(chat_id)
    await update.effective_message \
        .reply_text("Рад что вы с нами!) Сегодня отличный день чтоб поработать ;)")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    db = DB()
    db.stop_timer(chat_id)
    await update.message \
        .reply_text("Ну что ж) до следующего раза!")


##########


def bootstrap():
    # WorkTimerInstance = WorkTimer()
    application = ApplicationBuilder().token(config.telegram_bot_token).build()
    job_queue = application.job_queue
    job_minute = job_queue.run_repeating(alarm, interval=60, first=10)

    # application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("start", run))
    application.add_handler(CommandHandler("run", run))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("ostanovis", stop))

    # application.add_handler(CommandHandler('run', WorkTimerInstance.run))
    application.run_polling()
