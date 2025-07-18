from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import datetime
import pytz
from keep_alive import keep_alive
import os
keep_alive()

token: Final = os.environ.get('TOKEN', '')
bot_user: Final = '@tyshibot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("whats good")
    # Store the chat_id for reminders
    if isinstance(context.chat_data, dict):
        context.chat_data['remind'] = True

async def send_streak_reminder(application: Application):
    tz = pytz.timezone('Asia/Manila')
    while True:
        now = datetime.datetime.now(tz)
        # Calculate next 8pm
        next_8pm = now.replace(hour=20, minute=0, second=0, microsecond=0)
        if now >= next_8pm:
            next_8pm += datetime.timedelta(days=1)
        wait_seconds = (next_8pm - now).total_seconds()
        await asyncio.sleep(wait_seconds)
        for chat_id, chat_data in application.chat_data.items():
            if isinstance(chat_data, dict) and chat_data.get('remind'):
                try:
                    await application.bot.send_message(chat_id=chat_id, text="streak")
                except Exception as e:
                    print(f"Failed to send to {chat_id}: {e}")
        # Wait 60 seconds before checking again (avoid double send)
        await asyncio.sleep(60)

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start_command))

    async def post_init(application):
        application.create_task(send_streak_reminder(application))

    app.post_init = post_init
    app.run_polling()