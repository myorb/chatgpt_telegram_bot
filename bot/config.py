import yaml
from pathlib import Path
import os

telegram_token = os.environ.get("TELEGRAM_TOKEN")
openai_api_key = os.environ.get("OPENAI_API_KEY")
mongodb_uri = os.environ.get("MONGODB_URL")

if mongodb_uri is None:
    raise ValueError("Please set the environment variable 'telegram_token'") 

# config_dir = Path(__file__).parent.resolve() / "config"

# # load yaml config
# with open(config_dir / "config.yml", 'r') as f:
#     config_yaml = yaml.safe_load(f)

# load .env config
# config_env = dotenv.dotenv_values(config_dir / "config.env")

# config parameters
# telegram_token = config_yaml["telegram_token"]
# openai_api_key = config_yaml["openai_api_key"]
# mongodb_uri = f"mongodb://mongo:{config_env['MONGODB_PORT']}"


# openai_api_base = config_yaml.get("openai_api_base", None)
# allowed_telegram_usernames = config_yaml["allowed_telegram_usernames"]
# new_dialog_timeout = config_yaml["new_dialog_timeout"]
# enable_message_streaming = config_yaml.get("enable_message_streaming", True)
# return_n_generated_images = config_yaml.get("return_n_generated_images", 1)
# image_size = config_yaml.get("image_size", "512x512")
# n_chat_modes_per_page = config_yaml.get("n_chat_modes_per_page", 5)

# chat_modes
# with open(config_dir / "chat_modes.yml", 'r') as f:
#     chat_modes = yaml.safe_load(f)

# # models
# with open(config_dir / "models.yml", 'r') as f:
#     models = yaml.safe_load(f)

openai_api_base: null  # leave null to use default api base or you can put your own base url here
allowed_telegram_usernames: []  # if empty, the bot is available to anyone. pass a username string to allow it and/or user ids as positive integers and/or channel ids as negative integers
new_dialog_timeout: 600  # new dialog starts after timeout (in seconds)
return_n_generated_images: 1
n_chat_modes_per_page: 5
image_size: "512x512" # the image size for image generation. Generated images can have a size of 256x256, 512x512, or 1024x1024 pixels. Smaller sizes are faster to generate.
enable_message_streaming: true  # if set, messages will be shown to user word-by-word

# prices
chatgpt_price_per_1000_tokens: 0.002
gpt_price_per_1000_tokens: 0.02
whisper_price_per_1_min: 0.006


models = {
    "available_text_models": [
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "gpt-4-1106-preview",
        "gpt-4-vision-preview",
        "gpt-4",
        "text-davinci-003",
        "gpt-4o"
    ],
    "info": {
        "gpt-3.5-turbo": {
            "type": "chat_completion",
            "name": "ChatGPT",
            "description": "ChatGPT is that well-known model. It's <b>fast</b> and <b>cheap</b>. Ideal for everyday tasks. If there are some tasks it can't handle, try the <b>GPT-4</b>.",
            "price_per_1000_input_tokens": 0.0015,
            "price_per_1000_output_tokens": 0.002,
            "scores": {
                "Smart": 3,
                "Fast": 5,
                "Cheap": 5
            }
        },
        "gpt-3.5-turbo-16k": {
            "type": "chat_completion",
            "name": "GPT-16K",
            "description": "ChatGPT is that well-known model. It's <b>fast</b> and <b>cheap</b>. Ideal for everyday tasks. If there are some tasks it can't handle, try the <b>GPT-4</b>.",
            "price_per_1000_input_tokens": 0.003,
            "price_per_1000_output_tokens": 0.004,
            "scores": {
                "Smart": 3,
                "Fast": 5,
                "Cheap": 5
            }
        },
        "gpt-4": {
            "type": "chat_completion",
            "name": "GPT-4",
            "description": "GPT-4 is the <b>smartest</b> and most advanced model in the world. But it is slower and not as cost-efficient as ChatGPT. Best choice for <b>complex</b> intellectual tasks.",
            "price_per_1000_input_tokens": 0.03,
            "price_per_1000_output_tokens": 0.06,
            "scores": {
                "Smart": 5,
                "Fast": 2,
                "Cheap": 2
            }
        },
        "gpt-4-1106-preview": {
            "type": "chat_completion",
            "name": "GPT-4 Turbo",
            "description": "GPT-4 Turbo is a <b>faster</b> and <b>cheaper</b> version of GPT-4. It's as smart as GPT-4, so you should use it instead of GPT-4.",
            "price_per_1000_input_tokens": 0.01,
            "price_per_1000_output_tokens": 0.03,
            "scores": {
                "smart": 5,
                "fast": 4,
                "cheap": 3
            }
        },
        "gpt-4-vision-preview": {
            "type": "chat_completion",
            "name": "GPT-4 Vision",
            "description": "Ability to <b>understand images</b>, in addition to all other GPT-4 Turbo capabilties.",
            "price_per_1000_input_tokens": 0.01,
            "price_per_1000_output_tokens": 0.03,
            "scores": {
                "smart": 5,
                "fast": 4,
                "cheap": 3
            }
        },
        "gpt-4o": {
            "type": "chat_completion",
            "name": "GPT-4o",
            "description": "GPT-4o is a special variant of GPT-4 designed for optimal performance and accuracy. Suitable for complex and detailed tasks.",
            "price_per_1000_input_tokens": 0.03,
            "price_per_1000_output_tokens": 0.06,
            "scores": {
                "smart": 5,
                "fast": 2,
                "cheap": 2
            }
        },
        "text-davinci-003": {
            "type": "completion",
            "name": "GPT-3.5",
            "description": "GPT-3.5 is a legacy model. Actually there is <b>no reason to use it</b>, because it is more expensive and slower than ChatGPT, but just about as smart.",
            "price_per_1000_input_tokens": 0.02,
            "price_per_1000_output_tokens": 0.02,
            "scores": {
                "Smart": 3,
                "Fast": 2,
                "Cheap": 3
            }
        },
        "dalle-2": {
            "type": "image",
            "price_per_1_image": 0.018
        },
        "whisper": {
            "type": "audio",
            "price_per_1_min": 0.006
        }
    }
}


# files
# help_group_chat_video_path = Path(__file__).parent.parent.resolve() / "static" / "help_group_chat.mp4"
# help_group_chat_video_path = Path(__file__).parent.parent.resolve() / "static" / "help_group_chat.mp4"
