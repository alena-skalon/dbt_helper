"""
OpenRouter API integration service.
Handles communication with DeepSeek model through OpenRouter.
"""
import logging
import aiohttp
import asyncio
import socket
from typing import Optional

from config.settings import OPENROUTER_API_KEY

logger = logging.getLogger(__name__)

# Primary and backup API URLs
OPENROUTER_API_URLS = [
    "https://api.openrouter.ai/api/v1/chat/completions",
    "https://openrouter.ai/api/v1/chat/completions"  # Backup URL
]

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
        "Content-Type": "application/json",
        "OpenAI-Organization": "org-123",  # Required by OpenRouter
        "User-Agent": "DeepSeek Psychological Bot/1.0",
        "Host": "api.openrouter.ai"  # Explicitly set Host header
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
        "max_tokens": 1000,
        "stream": False
    }

    last_error = None
    # Try DNS resolution first
    try:
        logger.info("Attempting to resolve api.openrouter.ai...")
        ip_address = socket.gethostbyname("api.openrouter.ai")
        logger.info(f"Successfully resolved api.openrouter.ai to {ip_address}")
    except socket.gaierror as e:
        logger.error(f"DNS resolution failed: {str(e)}")
        
    # Try each API URL
    for api_url in OPENROUTER_API_URLS:
        try:
            logger.info(f"Trying API URL: {api_url}")
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(
                        api_url,
                        headers=headers,
                        json=data,
                        timeout=30,
                        ssl=True
                    ) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            logger.error(
                                "OpenRouter API error: Status: %d, Response: %s, Headers: %s", 
                                response.status,
                                error_text,
                                dict(response.headers)
                            )
                            raise DeepSeekError(f"API returned status {response.status}: {error_text}")
                        
                        result = await response.json()
                        logger.info("Successfully received response from OpenRouter API")
                        return result["choices"][0]["message"]["content"]
                        
                except aiohttp.ClientError as e:
                    last_error = e
                    logger.error(
                        "Network error details - Type: %s, Message: %s, Args: %s", 
                        type(e).__name__, 
                        str(e), 
                        getattr(e, 'args', [])
                    )
                    continue  # Try next URL
                except asyncio.TimeoutError as e:
                    last_error = e
                    logger.error("Request timed out after 30 seconds")
                    continue  # Try next URL
                    
        except Exception as e:
            last_error = e
            logger.error(
                "Unexpected error while calling OpenRouter - Type: %s, Message: %s", 
                type(e).__name__, 
                str(e)
            )
            continue  # Try next URL
            
    # If we get here, all URLs failed
    if last_error:
        raise DeepSeekError("Ошибка сети при обращении к API") from last_error 