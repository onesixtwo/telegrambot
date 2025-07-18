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
    while True:
        await asyncio.sleep(30)
        for chat_id, chat_data in application.chat_data.items():
            if isinstance(chat_data, dict) and chat_data.get('remind'):
                try:
                    await application.bot.send_message(chat_id=chat_id, text="streak")
                except Exception as e:
                    print(f"Failed to send to {chat_id}: {e}")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start_command))

    async def post_init(application):
        application.create_task(send_streak_reminder(application))

    app.post_init = post_init
    app.run_polling()