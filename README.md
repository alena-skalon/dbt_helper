# DeepSeek Psychological Telegram Bot

MVP психологического чат-бота на базе LLM (DeepSeek), доступного через Telegram.

## Основные функции
- Приём и отправка сообщений через Telegram
- Интеграция с DeepSeek API для генерации ответов
- Простой диалоговый интерфейс

## Быстрый старт
1. Клонируйте репозиторий
2. Установите зависимости:
   ```
   pip install -r deployment/requirements.txt
   ```
3. Создайте файл `.env` в папке `config` с переменными:
   - `TELEGRAM_TOKEN=...`
   - `DEEPSEEK_API_KEY=...`
4. Запустите бота:
   ```
   python main.py
   ```

## Деплой на Railway
- Используйте `deployment/Procfile` и requirements.txt
- Задайте переменные окружения через интерфейс Railway

---

> Проект для быстрого MVP. История сообщений и медиа не поддерживаются. 