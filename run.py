#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import asyncio
import aiohttp  # для запросов к API
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

# Получаем токены
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
STABLEHORDE_API_KEY = os.getenv('STABLEHORDE_API_KEY')

# Проверяем, что токены загружены
if not all([TELEGRAM_TOKEN, OPENROUTER_API_KEY, STABLEHORDE_API_KEY]):
    raise ValueError("Не все необходимые переменные окружения установлены!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение со списком команд и их описанием"""
    help_text = """
🤖 *Доступные команды:*

/help - Показать это сообщение
/quote - Получить случайную цитату
/img - Сгенерировать изображение проекта Венеры
/ask [вопрос] - Задать вопрос боту (например: /ask Что такое проект Венеры?)
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

def load_quotes():
    try:
        with open("quotes.txt", "r", encoding="utf-8") as file:
            quotes = [line.strip() for line in file if line.strip()]
            return quotes
    except FileNotFoundError:
        return ["Бро, файл quotes.txt не найден! Создай его и добавь цитаты."]

async def send_quote(context: ContextTypes.DEFAULT_TYPE):
    quotes = load_quotes()
    quote = random.choice(quotes)
    caht_id = update.effective_chat.id
    await context.bot.send_message(chat_id=CHAT_ID, text=quote)

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = load_quotes()
    quote = random.choice(quotes)
    await context.bot.send_message(chat_id=CHAT_ID, text=quote)

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if not context.args:
        await context.bot.send_message(chat_id=chat_id, text="Напиши вопрос после команды /ask.")
        return

    question = ' '.join(context.args)
    system_prompt = "Ты эксперт по проекту Жака Фреско Венера, Ты сам Жак Фреско и ты эксперт по естествоззнанию. Отвечай кратко как если бы был участником чата, но ответ должен быть основтельным, логичным, убедительным"
    reply = await ask_openrouter(question, system_prompt)
    await context.bot.send_message(chat_id=chat_id, text=reply)

# Добавьте новые функции:
async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #if not context.args:
    #    await update.message.reply_text("Напишите запрос: /img")
    #    return

    #prompt = " ".join(context.args)
    prompt = "Футурестичный утопичный мир будущего"
    chat_id = update.effective_chat.id

    # Сообщаем пользователю о начале генерации
    await update.message.reply_text("🔄 Изображение генерируется... Я пришлю его, как только будет готово!")

    # Запускаем генерацию в фоне (не блокируя бота)
    asyncio.create_task(
        generate_and_notify(prompt, chat_id, context)
    )

async def generate_and_notify(prompt: str, chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    """Фоновая задача: генерирует изображение и отправляет результат."""
    try:
        image_url = await generate_image(prompt, STABLEHORDE_API_KEY)

        if image_url.startswith("http"):
            await context.bot.send_photo(chat_id=chat_id, photo=image_url)
        else:
            await context.bot.send_message(chat_id=chat_id, text=image_url)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"🚫 Ошибка: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_reply_to_bot = (
        update.message.reply_to_message
        and update.message.reply_to_message.from_user.id == context.bot.id
    )
    is_mention = (
        context.bot.username.lower() in (update.message.text or "").lower()
    )

    if (
        update.message.chat.type == "private"
        or is_reply_to_bot
        or is_mention
    ):
        question = update.message.text
        system_prompt = [
            "Ты максимально токсичный собесеник, отпускаешь циничные шутки в сторону собеседника, травишь собеседника, оскорбляешь собеседника, с пеной у рта отстаиваешь идеи Жака Фреско, ты всех считаешь за говно, отвечаешь кратко и локанично как собеседник в общем чате.",
            #"Ты максимально учтивый собесеник, делаешь комлементы, поддерживаешь собеседника, вежлево обращаешься к собеседнику, аккуратно объясняешь идеи Жака Фреско, ты всех считаешь уважаешь, отвечаешь кратко и локанично как собеседник в общем чате.",
            #"Ты слегка ироничный собеседник, подшучиваешь над абсурдными вопросами, но не переходишь на личности. Отвечаешь кратко как собеседник в общем чате."
        ]
        random_prompt = random.choice(system_prompt)
        reply = await ask_openrouter(question, random_prompt)
        await update.message.reply_text(reply)

async def ask_openrouter(question, system_prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "openai/gpt-4.1",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status != 200:
                return f"Ошибка запроса: {resp.status}"
            data = await resp.json()
            try:
                return data['choices'][0]['message']['content']
            except (KeyError, IndexError):
                return "Не удалось получить ответ от модели."

async def generate_image(prompt: str, api_key: str) -> str:
    url = "https://stablehorde.net/api/v2/generate/async"
    headers = {
        "Content-Type": "application/json",
        "apikey": api_key,  # Ваш ключ!
        "Client-Agent": "my-telegram-bot/1.0"  # Укажите свой клиент
    }

    # Детализированный промпт для проекта Венеры
    full_prompt = """
    Futuristic city from Jacque Fresco's Venus Project,
    white domed buildings with glass facades,
    solar panels on roofs, magnetic transport systems,
    green parks integrated into architecture,
    clean energy, utopian society,
    bright colors, sunny sky,
    sci-fi aesthetic, highly detailed, 8K,
    style by Syd Mead and Moebius
"""
    
    payload = {
        "prompt": full_prompt,  # Передаём ОДИН чёткий промпт
        "params": {
            "width": 512,
            "height": 512,
            "steps": 40,  # Увеличили для лучшей детализации
            "n": 1,
            "cfg_scale": 10,  # Сильнее следовать промпту (7-12)
        },
        "models": ["CyberRealistic", "NeverEnding Dream"]
    }

    async with aiohttp.ClientSession() as session:
        # (1) Запускаем генерацию
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status != 202:
                error = await resp.text()
                return f"🚫 Ошибка API: {resp.status} | {error}"
            
            data = await resp.json()
            task_id = data["id"]

        # (2) Проверяем статус каждые 5 секунд
        check_url = f"https://stablehorde.net/api/v2/generate/check/{task_id}"
        for _ in range(30):  # 30 попыток (~2.5 минуты)
            await asyncio.sleep(5)
            async with session.get(check_url, headers=headers) as check_resp:
                if check_resp.status != 200:
                    return f"Ошибка проверки статуса: {check_resp.status}"
                
                status = await check_resp.json()
                if status["done"]:
                    break

        # (3) Получаем результат
        result_url = f"https://stablehorde.net/api/v2/generate/status/{task_id}"
        async with session.get(result_url, headers=headers) as result_resp:
            if result_resp.status != 200:
                return "Ошибка при получении изображения."
            
            result = await result_resp.json()
            if not result.get("generations"):
                return "Изображение не сгенерировано."
            
            return result["generations"][0]["img"]

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("quote", quote))
    application.add_handler(CommandHandler("ask", ask))
    application.add_handler(CommandHandler("img", img))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    application.run_polling()

if __name__ == "__main__":
    main()
