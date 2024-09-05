import os
import openai
import requests

import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

# Set up your environment variables (from DigitalOcean App Platform)
TELEGRAM_TOKEN = os.getenv("telegram_token")
OPENAI_API_KEY = os.getenv("openai_api_key")

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY
# Define the start command handler
# async def start(update: Update, context: CallbackContext):
#     await update.message.reply_text("Hello! I'm a bot that proxies your message to OpenAI. Type something to start!")

# # Define the handler for streaming OpenAI response
# async def stream_openai_response(update: Update, context: CallbackContext):
#     user_message = update.message.text

#     try:
#         # Send user message to OpenAI API with streaming enabled
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": user_message},
#             ],
#             stream=True,
#         )

#         final_response = ""
#         for chunk in response:
#             if 'choices' in chunk:
#                 delta = chunk['choices'][0]['delta']
#                 if 'content' in delta:
#                     final_response += delta['content']
#                     await update.message.reply_text(delta['content'], quote=False)

#     except Exception as e:
#         print(f"Error communicating with OpenAI: {e}")
#         await update.message.reply_text("Sorry, something went wrong.")

# # Main function to run the bot
# async def main():
#     # Create the Application and pass it the bot's token
#     application = Application.builder().token(TELEGRAM_TOKEN).build()

#     # Register the command and message handlers
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, stream_openai_response))

#     # Start the bot using long polling
#     await application.run_polling()

# if __name__ == '__main__':
#     import asyncio
#     asyncio.run(main())

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Send user message to OpenAI API with streaming enabled
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
            stream=True,
        )

        final_response = ""
        for chunk in response:
            if 'choices' in chunk:
                delta = chunk['choices'][0]['delta']
                if 'content' in delta:
                    final_response += delta['content']
                    await update.message.reply_text(delta['content'], quote=False)

    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        await update.message.reply_text("Sorry, something went wrong.")


if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, stream_openai_response))

    application.run_polling()