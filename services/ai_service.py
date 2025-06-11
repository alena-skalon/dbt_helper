"""
AI service integration.
Handles communication with the AI model API.
"""
import logging
import aiohttp
import asyncio
from typing import Optional

from config.settings import AI_API_KEY

logger = logging.getLogger(__name__)

API_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MAX_MESSAGE_LENGTH = 2000  # Maximum length of message to process

SYSTEM_PROMPT = """Adopt the role of a psychologist trained in DBT and ACT. 
Give me empathic and encouraging answer. Provide one non-banal, deep suggestion for how I can feel better right now. Reply in user's language"""

FALLBACK_MESSAGE = """Извините, но в данный момент я не могу обработать ваше сообщение, так как сервис AI недоступен.

Пожалуйста, попробуйте позже или обратитесь к администратору бота."""

class AIServiceError(Exception):
    """Base exception for AI service errors."""
    pass

class MessageTooLongError(AIServiceError):
    """Exception raised when message exceeds maximum length."""
    pass

class AIServiceUnavailableError(AIServiceError):
    """Exception raised when AI service is not configured."""
    pass

async def get_ai_response(message: str) -> str:
    """
    Send message to AI model API and get response.
    
    Args:
        message: User's message text
        
    Returns:
        str: Model's response text
        
    Raises:
        MessageTooLongError: If message exceeds maximum length
        AIServiceError: If API call fails
        AIServiceUnavailableError: If AI service is not configured
    """
    if not AI_API_KEY:
        logger.error("Cannot process message: AI_API_KEY is not set")
        return FALLBACK_MESSAGE
        
    if len(message) > MAX_MESSAGE_LENGTH:
        raise MessageTooLongError(
            f"Сообщение слишком длинное. Максимальная длина: {MAX_MESSAGE_LENGTH} символов."
        )
    
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "HTTP-Referer": "https://github.com/alena-skalon/dbt_helper",  # For rankings
        "X-Title": "DBT Helper Bot",  # For rankings
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000,
        "stream": False
    }

    try:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    API_BASE_URL,
                    headers=headers,
                    json=data,
                    timeout=30,
                    ssl=True
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(
                            "AI API error: Status: %d, Response: %s", 
                            response.status,
                            error_text
                        )
                        raise AIServiceError(f"API returned status {response.status}: {error_text}")
                    
                    result = await response.json()
                    logger.info("Successfully received response from AI API")
                    return result["choices"][0]["message"]["content"]
                    
            except aiohttp.ClientError as e:
                logger.error(
                    "Network error details - Type: %s, Message: %s", 
                    type(e).__name__, 
                    str(e)
                )
                raise AIServiceError("Ошибка сети при обращении к API") from e
            except asyncio.TimeoutError as e:
                logger.error("Request timed out after 30 seconds")
                raise AIServiceError("Превышено время ожидания ответа от API") from e
                
    except Exception as e:
        logger.error(
            "Unexpected error while calling AI API - Type: %s, Message: %s", 
            type(e).__name__, 
            str(e)
        )
        raise AIServiceError("Неожиданная ошибка при обработке запроса") from e 