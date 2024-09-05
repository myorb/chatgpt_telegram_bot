import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_TOKEN = os.getenv("telegram_token")
OPENAI_API_KEY = os.getenv("openai_api_key")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}],
        stream=True,
    )

    async for chunk in stream:
        response_content = chunk.choices[0].message.content
        print(response_contentt or "", end="")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response_content)

if __name__ == '__main__':
    application = ApplicationBuilder().token('TELEGRAM_TOKEN').build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()

# import os
# import asyncio
# import logging
# from openai import AsyncOpenAI
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# # Environment variables for the API keys
# TELEGRAM_TOKEN = os.getenv("telegram_token")
# OPENAI_API_KEY = os.getenv("openai_api_key")

# # Set up logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )

# # Initialize AsyncOpenAI client with API key
# client = OpenAI(api_key=OPENAI_API_KEY)

# # Handler for the /start command
# def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a bot that proxies your messages to OpenAI. Type something to start!")

# # Handler for streaming OpenAI responses
# def stream_openai_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_message = update.message.text  # The message from the user

#     try:
#         # Send the message to OpenAI and enable streaming
#         stream = await client.chat.completions.create(
#             model="gpt-4",
#             messages=[{"role": "user", "content": user_message}],
#             stream=True,  # Enable streaming
#         )

#         bot_reply = response['choices'][0]['message']['content']
#         logger.info(f"OpenAI response: {bot_reply}")
#         update.message.reply_text(bot_reply)

#     except Exception as e:
#         logging.error(f"Error communicating with OpenAI: {e}")
#         await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, something went wrong.")

# # Main function to initialize the bot and register handlers
# def main():
#     # Initialize the Telegram bot application
#     application = Application.builder().token(TELEGRAM_TOKEN).build()

#     # Register handlers for the /start command and incoming text messages
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), stream_openai_response))

#     # Start polling for new messages
#     await application.run_polling()

# if __name__ == '__main__':
#     main()