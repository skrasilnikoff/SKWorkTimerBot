# import json
# from typing import Union, Any
import random

import config
import datetime

from ai import AI_Bot
from db import DB

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, MessageHandler, filters

TELEGRAM_BOT_TOKEN = config.telegram_bot_token

ai_bot = AI_Bot(base_url="http://localhost:1234/v1", api_key="lm-studio")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка входящих сообщений."""
    if update.message is not None:
        user_message = update.message.text
        print(user_message)
        response = ai_bot.generate_response_with_prev(user_message)
        if response.strip() != "":
            await update.message.reply_text(response)


async def handle_message_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка входящих сообщений."""
    if update.message is not None:
        user_message = update.message.text
        user_message = f'Олег. {user_message}'
        print(user_message)
        response = ai_bot.generate_response(user_message)
        if response.strip() != "":
            await update.message.reply_text(response)


def get_currnet_day_of_week():
    now = datetime.datetime.now()
    weekdays = [
        'понедельник',  # Monday
        'вторник',  # Tuesday
        'среда',  # Wednesday
        'четверг',  # Thursday
        'пятница',  # Friday
        'суббота',  # Saturday
        'воскресенье'  # Sunday
    ]
    weekday_index = now.weekday()
    return weekdays[weekday_index]


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


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

        messages = []
        ai_message = ''

        if 45 == minutes:
            ai_message = "Олег, Напиши, что через 5 минут наступит перерыв, своими словами"
            messages = [
                'Перерыв через 5 минут',
                'Скоро отдохнем)',
                'Вот вот перерыв!'
            ]

        if 50 == minutes:
            ai_message = "Олег, Напиши, что пришло время перерыва, своими словами"
            messages = [
                'Давайте прервемся )',
                'Перерыв)',
                'Го отдохнем',
                'Время отдохнуть немножечко'
            ]

        if 00 == minutes:
            ai_message = "Олег, Напиши, что пришло время продолжать работать, своими словами"
            messages = [
                'Пора работать! =)',
                'Время сделать много денюжек)',
                'Ну что, погнали!',
                'Не расслабляться!'
            ]

        if messages:
            message = random.choice(messages)
            print("message", message)

            print("ai_message prompt >>", ai_message)
            ai_message = ai_bot.generate_response(ai_message)
            print("ai_message response <<", ai_message)
            if ai_message:
                message = ai_message
            
            await context.bot.send_message(chat_id, text=message)

            # message = f'=== {message} ===\n\n{ai_message}'
            # await context.bot.send_message(chat_id, text=ai_message)


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    db = DB()
    db.start_timer(chat_id)
    day = get_currnet_day_of_week()

    message = f"Сегодня {day} и это отличный день чтоб поработать! ;)"

    if day == 'пятница':
        message = f"Наконец {day}! Хорошо поработаем и отдыхать!)"

    message = f"Рад что вы с нами!) {message}"

    ai_message = ai_bot.generate_response(
        f'Олег, перефразируй следующую фразу: "{message}". Напиши свой лучший вариант, от первого лица, чтобы звучало как твоя собственная мысль.')

    await update.effective_message \
        .reply_text(ai_message)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    db = DB()
    db.stop_timer(chat_id)

    message = "Ну что ж. до следующего раза!"
    ai_message = ai_bot.generate_response(
        f'Олег, перефразируй следующую фразу: "{message}". Напиши свой лучший вариант, от первого лица, чтобы звучало как твоя собственная мысль.')

    await update.message \
        .reply_text(ai_message)


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

    # reply_filter = filters.REPLY & filters.UpdateType.MESSAGE
    reply_filter = filters.TEXT  # & filters.UpdateType.MESSAGE
    application.add_handler(MessageHandler(reply_filter, handle_message))

    application.run_polling()
