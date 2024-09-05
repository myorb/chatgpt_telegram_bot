import os
import openai
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up your environment variables (from DigitalOcean App Platform)
TELEGRAM_TOKEN = os.getenv("telegram_token")
OPENAI_API_KEY = os.getenv("openai_api_key")

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY

# Initialize Telegram bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I'm a bot that proxies your message to OpenAI. Type something to start!")

def stream_openai_response(update: Update, context: CallbackContext):
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
                    update.message.reply_text(delta['content'], quote=False)

    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        update.message.reply_text("Sorry, something went wrong.")

def main():
    # Create the Updater and pass it the bot's token
    updater = Updater(TELEGRAM_TOKEN)

    # Register command and message handlers
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, stream_openai_response))

    # Start polling Telegram for new messages (long polling)
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
