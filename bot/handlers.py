"""
Telegram bot message handlers.
Includes command handlers and message processors.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes

from config.settings import WELCOME_MESSAGE
from services.deepseek import get_deepseek_response, MessageTooLongError, DeepSeekError

logger = logging.getLogger(__name__)

WELCOME_MESSAGE = """👋 Привет! Я бот-психолог, обученный методам DBT (Диалектическая поведенческая терапия) и ACT (Терапия принятия и ответственности).

🤝 Я здесь, чтобы выслушать тебя и помочь:
- Разобраться в сложных эмоциях
- Найти новые способы справляться с трудностями
- Получить поддержку и практические советы

💭 Просто напиши мне о том, что тебя беспокоит или что ты чувствуешь.

📌 Используй /help чтобы узнать больше о том, как я могу помочь."""

HELP_MESSAGE = """🌟 Как я могу помочь:

1️⃣ Поделись своими мыслями и чувствами
   Просто напиши мне о том, что тебя беспокоит

2️⃣ Получи эмпатичный ответ
   Я внимательно выслушаю и постараюсь понять твои чувства

3️⃣ Практические рекомендации
   Я предложу конкретные техники из DBT и ACT

📝 Примеры обращений:
- "Я чувствую тревогу из-за предстоящего собеседования"
- "Мне сложно справиться с раздражением на коллег"
- "Я часто себя критикую и не знаю, как с этим быть"

🔄 Команды:
/start - Начать диалог
/help - Показать это сообщение

💡 Помни: я не заменяю профессионального психолога, но могу поддержать тебя и предложить полезные инструменты для работы с эмоциями."""

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    user = update.effective_user
    logger.info("User %s started the bot", user.id)
    await update.message.reply_text(WELCOME_MESSAGE)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    user = update.effective_user
    logger.info("User %s requested help", user.id)
    await update.message.reply_text(HELP_MESSAGE)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages."""
    user = update.effective_user
    message_text = update.message.text
    
    logger.info("Received message from user %s: %s", user.id, message_text)
    
    try:
        # Send typing action while processing
        await update.message.chat.send_action("typing")
        
        # Get response from DeepSeek
        response = await get_deepseek_response(message_text)
        
        await update.message.reply_text(response)
        logger.info("Sent response to user %s", user.id)
        
    except MessageTooLongError as e:
        error_message = str(e)
        logger.warning("Message too long from user %s", user.id)
        await update.message.reply_text(error_message)
    except DeepSeekError as e:
        error_message = (
            "😔 Извините, произошла ошибка при обработке вашего сообщения.\n"
            "Пожалуйста, попробуйте позже или напишите другое сообщение."
        )
        logger.error("API error for user %s: %s", user.id, str(e))
        await update.message.reply_text(error_message)
    except Exception as e:
        error_message = "😔 Произошла неожиданная ошибка. Пожалуйста, попробуйте позже."
        logger.error("Unexpected error for user %s: %s", user.id, str(e))
        await update.message.reply_text(error_message) 