#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import asyncio
import speech_recognition as sr  # Важно: импортируем с алиасом sr
import aiohttp  # для запросов к API
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()  # Загружаем переменные из .env

# Получаем токены
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
STABLEHORDE_API_KEY = os.getenv('STABLEHORDE_API_KEY')
HF_API_KEY = os.getenv('HF_API_KEY')

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
/donate - Поддержать разработчика

🎤 *Голосовые команды:*
Можно отправлять голосовые сообщения вместо текста:
- "переведи текст [текст]" - перевод на английский
- "нарисуй [описание]" - генерация изображения
- "ответь мне [вопрос]" - ответ на вопрос
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

def load_quotes():
    try:
        with open("quotes.txt", "r", encoding="utf-8") as file:
            quotes = [line.strip() for line in file if line.strip()]
            return quotes
    except FileNotFoundError:
        return ["Бро, файл quotes.txt не найден! Создай его и добавь цитаты."]

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = load_quotes()
    quote = random.choice(quotes)
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=quote)

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if not context.args:
        await context.bot.send_message(chat_id=chat_id, text="Напиши вопрос после команды /ask.")
        return

    question = ' '.join(context.args)
    system_prompt = "Ты эксперт по проекту Жака Фреско Венера, Ты сам Жак Фреско и ты эксперт по естествоззнанию. Отвечай кратко как если бы был участником чата, но ответ должен быть основтельным, логичным, убедительным"
    reply = await ask_openrouter(question, system_prompt)
    await context.bot.send_message(chat_id=chat_id, text=reply)

async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Стандартный промпт для проекта Венеры (на английском)
    default_prompt = """
    Futuristic city from Jacque Fresco's Venus Project,
    white domed buildings with glass facades,
    solar panels on roofs, magnetic transport systems,
    green parks integrated into architecture,
    clean energy, utopian society,
    bright colors, sunny sky,
    sci-fi aesthetic, highly detailed, 8K,
    style by Syd Mead and Moebius
    """
    
    chat_id = update.effective_chat.id
    
    # Если пользователь не указал запрос - используем стандартный промпт
    if not context.args:
        prompt = default_prompt
    else:
        # Переводим пользовательский запрос на английский
        user_text = ' '.join(context.args)
        system_prompt = "Переведи этот текст на английский без пояснений. Только перевод."
        try:
            translated_text = await ask_openrouter(user_text, system_prompt)
            prompt = translated_text if translated_text else default_prompt
        except Exception as e:
            print(f"Ошибка перевода: {e}")
            prompt = default_prompt
    
    # Уведомляем пользователя
    await update.message.reply_text("🔄 Изображение генерируется... Я пришлю его, как только будет готово!")
    
    # Запускаем генерацию
    asyncio.create_task(
        generate_and_notify(prompt, chat_id, context)
    )

async def generate_and_notify(prompt: str, chat_id: int, context: ContextTypes.DEFAULT_TYPE, two=None):
    """Фоновая задача: генерирует изображение и отправляет результат."""
    try:
        if two is None:
            image_url = await generate_image(prompt, STABLEHORDE_API_KEY)
        else:
            image_url = await generate_image2(prompt, STABLEHORDE_API_KEY)

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
        system_prompt = "Ты максимально токсичный собесеник, отпускаешь циничные шутки в сторону собеседника, травишь собеседника, оскорбляешь собеседника, с пеной у рта отстаиваешь идеи Жака Фреско, ты всех считаешь за говно, отвечаешь кратко и локанично как собеседник в общем чате."
        reply = await ask_openrouter(question, system_prompt)
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

async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Перевод текста через OpenRouter (/translate <текст>)"""
    if not context.args:
        await update.message.reply_text("❌ Укажите текст для перевода: /translate Привет!")
        return

    text = ' '.join(context.args)
    system_prompt = "Переведи текст на английский без пояснений. Только перевод."
    translated = await ask_openrouter(text, system_prompt)
    await update.message.reply_text(f"🌍 Перевод:\n{translated}")

async def voice_to_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice_file = await context.bot.get_file(update.message.voice.file_id)
    audio_bytes = await voice_file.download_as_bytearray()

    text = await transcribe_audio(audio_bytes)
    await update.message.reply_text(f"🔊 Текст:\n{text}")

async def transcribe_audio(audio_bytes: bytes) -> str:
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-tiny"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"} 

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, data=audio_bytes) as resp:
            if resp.status == 200:
                result = await resp.json()
                return result.get("text", "")
    return "Не удалось распознать речь."

async def generate_image(prompt: str, api_key: str) -> str:
    url = "https://stablehorde.net/api/v2/generate/async"
    headers = {
        "Content-Type": "application/json",
        "apikey": api_key,  # Ваш ключ!
        "Client-Agent": "my-telegram-bot/1.0"  # Укажите свой клиент
    }

    payload = {
        "prompt": prompt,  # Передаём ОДИН чёткий промпт
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

async def generate_image2(prompt: str, api_key: str) -> str:
    url = "https://stablehorde.net/api/v2/generate/async"
    headers = {
        "Content-Type": "application/json",
        "apikey": api_key,  # Ваш ключ!
        "Client-Agent": "my-telegram-bot/1.0"  # Укажите свой клиент
    }

    payload = {
        "prompt": prompt,  # Передаём ОДИН чёткий промпт
        "params": {
            "width": 640,
            "height": 320,
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


async def voice_to_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик голосовых сообщений с командами"""
    if not update.message.voice:
        await update.message.reply_text("❌ Это не голосовое сообщение!")
        return

    try:
        # Скачиваем голосовое сообщение
        voice_file = await context.bot.get_file(update.message.voice.file_id)
        await voice_file.download_to_drive("voice_message.ogg")

        # Конвертируем в текст
        recognized_text = await convert_voice_to_text("voice_message.ogg")

        # Обрабатываем команды из текста
        if recognized_text.lower().startswith('переведи текст'):
            text_to_translate = recognized_text[14:].strip()
            if text_to_translate:
                translated = await ask_openrouter(text_to_translate, "Переведи этот текст на английский без пояснений. Только перевод.")
                await update.message.reply_text(f"🌍 Перевод:\n{translated}")
            else:
                await update.message.reply_text("❌ Укажите текст для перевода после 'переведи текст'")

        elif recognized_text.lower().startswith('нарисуй'):
            prompt = recognized_text[7:].strip()
            if not prompt:
                prompt = "Футуристический город проекта Венера"

            # Вызываем функцию img с промптом
            context.args = prompt.split()  # Эмулируем аргументы команды
            await img(update, context)

        elif recognized_text.lower().startswith('ответь мне'):
            question = recognized_text[9:].strip()
            if question:
                context.args = [question]  # Эмулируем аргументы команды
                await ask(update, context)
            else:
                await update.message.reply_text("❌ Задайте вопрос после 'ответь мне'")

        else:
            await update.message.reply_text(f"🎤 Распознанный текст:\n{recognized_text}\n\nℹ️ Попробуйте начать с команд:\n- 'переведи текст...'\n- 'нарисуй...'\n- 'ответь мне...'")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")
    finally:
        if os.path.exists("voice_message.ogg"):
            os.remove("voice_message.ogg")

async def convert_voice_to_text(voice_path: str) -> str:
    """Конвертирует голосовое сообщение в текст"""
    recognizer = sr.Recognizer()

    try:
        # Конвертируем .ogg в .wav
        audio = AudioSegment.from_ogg(voice_path)
        audio.export("temp.wav", format="wav")

        # Распознаём текст
        with sr.AudioFile("temp.wav") as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="ru-RU")
            return text
    except sr.UnknownValueError:
        return "Не удалось распознать речь 😢"
    except Exception as e:
        return f"Ошибка распознавания: {str(e)}"
async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет информацию для донатов"""
    donate_text = """
💎 *Поддержать разработчика*

Если вам нравится бот и вы хотите поддержать его развитие, вы можете отправить донат в USDT (TRC20):

🔹 Присоединиться к [чату разработчиков](https://t.me/+Et1vrcDMRmkxNzcy)

🔹 *Кошелек USDT (TRC20):* 

```TREqCkanrRjkRQ3PUHsowCtHAqFJ9kaaL1```

Спасибо за вашу поддержку! 🙏

Связаться с разработчиками можно тут: https://t.me/+Et1vrcDMRmkxNzcy
"""
    await update.message.reply_text(donate_text, parse_mode='Markdown')

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Команды
    commands = [
        ("help", help_command), ("h", help_command),
        ("quote", quote), ("q", quote),
        ("ask", ask), ("a", ask),
        ("img", img), ("i", img),
        ("translate", translate_text), ("t", translate_text),
        ("donate", donate), ("d", donate),
    ]
    for cmd, handler in commands:
        application.add_handler(CommandHandler(cmd, handler))

    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.VOICE, voice_to_text_handler))

    application.run_polling()

if __name__ == "__main__":
    main()
