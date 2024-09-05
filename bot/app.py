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
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message},
                ],
                "stream": True,
            },
            stream=True,
        )

        # Stream OpenAI response and send to Telegram in chunks
        final_response = ""
        for chunk in response.iter_lines():
            if chunk:
                decoded_chunk = chunk.decode("utf-8").replace("data: ", "")
                if decoded_chunk.strip() == "[DONE]":
                    break
                message_content = decoded_chunk.strip()
                if message_content:
                    try:
                        message_json = eval(message_content)
                        delta = message_json.get("choices")[0].get("delta", {}).get("content", "")
                        if delta:
                            final_response += delta
                            update.message.reply_text(delta, quote=False)
                    except Exception as e:
                        print(f"Error parsing chunk: {e}")
                        pass

    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        update.message.reply_text("Sorry, something went wrong.")

def main():
    # Create the Updater and pass it the bot's token
    updater = Updater(TELEGRAM_TOKEN)

    # Register command and message handlers
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, stream_openai_response))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
