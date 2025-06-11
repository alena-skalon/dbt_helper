"""
Configuration settings and environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable is not set")

# OpenRouter API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set")

# Bot settings
BOT_NAME = "DeepSeek Psychological Bot"
WELCOME_MESSAGE = """
👋 Привет! Я психологический чат-бот на базе DeepSeek.
Расскажите, что вас беспокоит, и я постараюсь помочь.

🔒 Ваши сообщения не сохраняются и не используются для обучения.
""" 