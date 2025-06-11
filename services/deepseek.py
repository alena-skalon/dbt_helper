"""
OpenRouter API integration service.
Handles communication with DeepSeek model through OpenRouter.
"""
import logging
import aiohttp
from typing import Optional

from config.settings import OPENROUTER_API_KEY

logger = logging.getLogger(__name__)

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MAX_MESSAGE_LENGTH = 2000  # Maximum length of message to process

SYSTEM_PROMPT = """Adopt the role of a psychologist trained in DBT and ACT. 
Give me empathic and encouraging answer. Provide one non-banal, deep suggestion for how I can feel better right now. Reply in user's language"""

class DeepSeekError(Exception):
    """Base exception for DeepSeek API errors."""
    pass

class MessageTooLongError(DeepSeekError):
    """Exception raised when message exceeds maximum length."""
    pass

async def get_deepseek_response(message: str) -> str:
    """
    Send message to DeepSeek model through OpenRouter API and get response.
    
    Args:
        message: User's message text
        
    Returns:
        str: Model's response text
        
    Raises:
        MessageTooLongError: If message exceeds maximum length
        DeepSeekError: If API call fails
    """
    if len(message) > MAX_MESSAGE_LENGTH:
        raise MessageTooLongError(
            f"Сообщение слишком длинное. Максимальная длина: {MAX_MESSAGE_LENGTH} символов."
        )
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/alena-skalon/dbt_helper",
        "X-Title": "DeepSeek Psychological Bot",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-ai/deepseek-chat-33b",
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
        "max_tokens": 1000
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                OPENROUTER_API_URL,
                headers=headers,
                json=data,
                timeout=30  # 30 seconds timeout
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(
                        "OpenRouter API error: %s (status: %d)", 
                        error_text, 
                        response.status
                    )
                    raise DeepSeekError(f"API returned status {response.status}")
                
                result = await response.json()
                return result["choices"][0]["message"]["content"]
                
    except aiohttp.ClientError as e:
        logger.error("Network error while calling OpenRouter: %s", str(e))
        raise DeepSeekError("Ошибка сети при обращении к API") from e
    except Exception as e:
        logger.error("Unexpected error while calling OpenRouter: %s", str(e))
        raise DeepSeekError("Неожиданная ошибка при обработке запроса") from e 