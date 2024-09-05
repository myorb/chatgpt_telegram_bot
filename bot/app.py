import os
import asyncio
import requests
import logging

from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("telegram_token")
OPENAI_API_KEY = os.getenv("openai_api_key")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def stream_openai_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Send user message to OpenAI API with streaming enabled
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
            stream=True,
        )

        async for chunk in stream:
            final_response = chunk.choices[0].delta.content or "", end=""
            print(final_response)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=final_response)

    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        await update.message.reply_text("Sorry, something went wrong.")


async def main():
    # Create the Application and pass it the bot's token
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register the command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), stream_openai_response))

    # Start the bot using long polling
    await application.run_polling()


if __name__ == '__main__':
    asyncio.run(main())