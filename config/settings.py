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

# AI API Key
AI_API_KEY = os.getenv("AI_API_KEY")
if not AI_API_KEY:
    raise ValueError("AI_API_KEY environment variable is not set")

# Bot settings
BOT_NAME = "Psychological Support Bot"
WELCOME_MESSAGE = """
👋 Привет! Я психологический чат-бот.
Расскажите, что вас беспокоит, и я постараюсь помочь.

🔒 Ваши сообщения не сохраняются и не используются для обучения.
""" 