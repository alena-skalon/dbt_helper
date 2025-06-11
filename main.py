"""
Main entry point for the Telegram bot.
Initializes the bot and starts polling for updates.
"""
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config.settings import TELEGRAM_TOKEN, BOT_NAME
from bot.handlers import start_command, help_command, handle_message

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Initialize and run the bot."""
    logger.info("Starting %s...", BOT_NAME)
    
    # Create the Application
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start polling
    logger.info("Bot is ready to handle messages!")
    application.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main() 