#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import asyncio
import yt_dlp
import speech_recognition as sr  # Важно: импортируем с алиасом sr
import aiohttp  # для запросов к API
import time
import traceback
import re
import uuid
import edge_tts
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from pydub import AudioSegment
from gtts import gTTS
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
/game - Играть в крестики-нолики прямо в Telegram

🎧 *Музыкальные команды:*
/play [название] - Найти и отправить трек (из YouTube)
/find [описание] - Найти музыку по описанию настроения (например: /find грустный джаз)

💡 Совет: Для лучшего качества указывайте исполнителя в запросе:
Пример: /play Pink Floyd - Time

📹 *Видео команды:*
/youtube <url> - cкачать видео с YouTube (до 50MB)
/twitter <url> - cкачать видео из Twitter/X
/tiktok <url> - видео из Tiktok
/vkclip <url> - скачать клип из vk 

🎤 *Голосовые команды:*
/say [текст] - Озвучить текст мужским голосом (только аудио)

Можно отправлять голосовые сообщения вместо текста:
- "переведи текст [текст]" - перевод на английский
- "нарисуй [описание]" - генерация изображения
- "ответь мне [вопрос]" - ответ на вопрос
- "Найди трек [название]" - поиск и воспроизведение музыки
- "Скажи" - озвучить голосовое сообщение
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

    # Автоопределение YouTube ссылок
    if "youtube.com" in update.message.text or "youtu.be" in update.message.text:
        context.args = [update.message.text]
        await download_youtube(update, context)
        return

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

        elif recognized_text.lower().startswith('найди трек'):
            query = recognized_text[10:].strip()  # Убираем "найди трек"
            if query:
                # Используем существующую функцию play_music
                context.args = query.split()  # Имитируем аргументы команды
                await play_music(update, context)
            else:
                await update.message.reply_text("Укажите название трека после 'найди трек'")

        elif recognized_text.lower().startswith('ответь мне'):
            question = recognized_text[9:].strip()
            if question:
                context.args = [question]  # Эмулируем аргументы команды
                await ask(update, context)
            else:
                await update.message.reply_text("❌ Задайте вопрос после 'ответь мне'")

        # Обрабатываем команду "скажи"
        elif recognized_text.lower().startswith('скажи'):
            query = recognized_text[5:].strip()
            if query:
                # Эмулируем команду /voice
                context.args = [query]
                await send_voice_message(update, context)
            else:
                await update.message.reply_text("❌ Укажите, что сказать после 'скажи'")

        else:
            await update.message.reply_text(f"🎤 Распознанный текст:\n{recognized_text}\n\nℹ️ Попробуйте начать с команд:\n- 'переведи текст...'\n- 'нарисуй...'\n- 'ответь мне...''\n- 'найди трек...'")

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

async def play_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажите название трека: /play <название>")
        return

    query = ' '.join(context.args)
    await update.message.reply_text(f"🔍 Ищу трек: {query}...")

    try:
        # Создаем папку downloads если ее нет
        os.makedirs('downloads', exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best',
            'default_search': 'ytsearch',
            'noplaylist': True,
            'quiet': True,
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'retries': 3,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)

            if not info or not info.get('entries'):
                await update.message.reply_text("Трек не найден")
                return

            # Получаем реальный путь к файлу
            original_filename = ydl.prepare_filename(info['entries'][0])
            audio_file = os.path.splitext(original_filename)[0] + '.mp3'

            # Ждем пока файл появится (макс 10 сек)
            for _ in range(10):
                if os.path.exists(audio_file):
                    break
                await asyncio.sleep(1)
            else:
                raise Exception("Файл не был создан")

            # Проверяем размер файла
            if not os.path.exists(audio_file) or os.path.getsize(audio_file) < 1024:
                raise Exception("Неверный размер файла")

            # Отправляем аудио
            with open(audio_file, 'rb') as audio:
                await update.message.reply_audio(
                    audio=audio,
                    title=info['entries'][0].get('title', query),
                    performer=info['entries'][0].get('uploader', 'Unknown Artist')
                )

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
        print(f"Error: {traceback.format_exc()}")

    finally:
        # Удаляем временные файлы
        if 'original_filename' in locals() and os.path.exists(original_filename):
            os.remove(original_filename)
        if 'audio_file' in locals() and os.path.exists(audio_file):
            os.remove(audio_file)

async def download_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажите URL YouTube видео: /download <url>")
        return

    url = context.args[0]
    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("Пожалуйста, укажите корректную ссылку на YouTube")
        return

    progress_message = None

    try:
        progress_message = await update.message.reply_text("⏳ Начинаю загрузку видео...")

        ydl_opts = {
            'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'quiet': True,
            'socket_timeout': 30,
            'retries': 3,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)

            file_size = os.path.getsize(video_path)
            if file_size > 50 * 1024 * 1024:
                raise Exception(f"Видео слишком большое ({file_size // (1024 * 1024)}MB). Макс. 50MB.")

            await progress_message.edit_text("📤 Отправляю видео...")

            # Исправленный вызов без параметра timeout
            await update.message.reply_video(
                video=open(video_path, 'rb'),
                caption=f"🎬 {info.get('title', 'Без названия')}",
                duration=info.get('duration'),
                supports_streaming=True
            )

    except Exception as e:
        error_msg = f"❌ Ошибка: {str(e)}"
        if progress_message:
            await progress_message.edit_text(error_msg)
        else:
            await update.message.reply_text(error_msg)
        print(f"Video download error: {traceback.format_exc()}")

    finally:
        if 'video_path' in locals() and os.path.exists(video_path):
            os.remove(video_path)
        if progress_message:
            try:
                await progress_message.delete()
            except:
                pass

async def download_twitter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажите URL твита с видео: /download_twitter <url>")
        return

    url = context.args[0]
    if "twitter.com" not in url and "x.com" not in url:
        await update.message.reply_text("Пожалуйста, укажите корректную ссылку на Twitter/X")
        return

    try:
        msg = await update.message.reply_text("⏳ Скачиваю видео из Twitter...")

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'merge_output_format': 'mp4',
            'cookiefile': 'cookies.txt',  # Для обхода ограничений (опционально)
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)

            await msg.edit_text("📤 Отправляю видео...")
            await update.message.reply_video(
                video=open(video_path, 'rb'),
                caption=f"🎬 Видео из Twitter\n@{info.get('uploader', 'unknown')}"
            )

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
        print(f"Twitter download error: {traceback.format_exc()}")

    finally:
        if 'video_path' in locals() and os.path.exists(video_path):
            os.remove(video_path)
        if 'msg' in locals():
            try:
                await msg.delete()
            except:
                pass

async def download_vk_clip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Сохраняем ID сообщения запроса для последующего удаления
    request_message = update.message

    if not context.args:
        await update.message.reply_text(
            "❌ Укажите URL клипа VK\nПример: /vkclip https://vk.com/clip-222106755_456254140")
        return

    url = context.args[0]
    processing_msg = await update.message.reply_text("⏳ Скачиваю клип из VK...")

    try:
        ydl_opts = {
            'format': 'best[height<=720]',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'extractor_args': {'vk': {'clip': True}}
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await processing_msg.edit_text("📤 Отправляю клип...")
        await request_message.delete()  # Удаляем сообщение с запросом

        await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=open(filename, 'rb'),
            caption=f"🎬 Клип: {info.get('title', 'Без названия')}",
            supports_streaming=True
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    finally:
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)
        await processing_msg.delete()
async def vk_playlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text("❌ Укажите URL плейлиста VK после команды")
            return

        url = context.args[0]

        # Проверка и преобразование ссылки
        if "vk.com/music/playlist/" in url:
            parts = url.split('/')
            owner_id = parts[-2].split('_')[0]
            playlist_id = parts[-2].split('_')[1]
            new_url = f"https://vk.com/audio?act=audio_playlist{owner_id}_{playlist_id}"
            await update.message.reply_text(f"🔗 Преобразованная ссылка: {new_url}")
            url = new_url

        if "audio_playlist" not in url:
            await update.message.reply_text(
                "⚠️ Это не ссылка на плейлист VK! Пример правильной ссылки:\nhttps://vk.com/audio?section=playlists&z=audio_playlist_123_456")
            return

        msg = await update.message.reply_text("🔍 Ищу плейлист... Это может занять до 1 минуты...")

        ydl_opts = {
            'extract_flat': 'in_playlist',
            'quiet': True,
            'force_generic_extractor': True,
            'cookiefile': 'cookies.txt',  # Рекомендуется для VK
            'extractor_args': {
                'vk': {
                    'username': 'ваш_логин',  # Опционально
                    'password': 'ваш_пароль'  # Опционально
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if not info or not info.get('entries'):
                await msg.edit_text(
                    "😢 Не удалось получить плейлист. Возможные причины:\n1. Плейлист приватный\n2. Требуется авторизация\n3. VK заблокировал запрос")
                return

            await msg.edit_text(f"🎵 Найдено треков: {len(info['entries'])}\nСкачиваю первые 3 трека...")

            for entry in info['entries'][:3]:  # Ограничение для теста
                try:
                    track_title = f"{entry.get('artist', '?')} - {entry.get('title', 'Без названия')}"
                    await msg.edit_text(f"⬇️ Загружаю: {track_title}")

                    audio_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': f"downloads/{entry['id']}.%(ext)s",
                        'quiet': True,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                        }],
                    }

                    with yt_dlp.YoutubeDL(audio_opts) as audio_ydl:
                        audio_info = audio_ydl.extract_info(entry['url'], download=True)
                        audio_file = audio_ydl.prepare_filename(audio_info).replace('.webm', '.mp3')

                        await update.message.reply_audio(
                            audio=open(audio_file, 'rb'),
                            title=entry.get('title'),
                            performer=entry.get('artist'),
                        )
                        os.remove(audio_file)

                except Exception as e:
                    await update.message.reply_text(f"❌ Ошибка загрузки трека: {str(e)}")
                    continue

        await msg.edit_text("✅ Готово! Для скачивания полного плейлиста используйте VPN или повторите позже")

    except Exception as e:
        await update.message.reply_text(
            f"🔥 Критическая ошибка: {str(e)}\nПопробуйте другой плейлист или повторите позже")
async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Укажите ссылку на TikTok видео после команды\nПример: /tiktok https://vm.tiktok.com/ZM6example/")
        return

    url = context.args[0]

    # Проверка валидности ссылки
    #if not re.match(r'https?://(vm\.tiktok\.com|www\.tiktok\.com)/', url):
    #    await update.message.reply_text("⚠️ Это не ссылка на TikTok видео!")
    #    return

    try:
        msg = await update.message.reply_text("⏳ Скачиваю видео с TikTok...")

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'merge_output_format': 'mp4',
            'extractor_args': {
                'tiktok': {
                    'headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            # Отправка видео
            await update.message.reply_video(
                video=open(filename, 'rb'),
                caption=f"🎵 {info.get('title', 'Видео с TikTok')}\n\n🔗 {url}",
                supports_streaming=True
            )

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
        print(f"TikTok download error: {traceback.format_exc()}")

    finally:
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)
        if 'msg' in locals():
            try:
                await msg.delete()
            except:
                pass
async def send_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Укажите текст после команды\nПример: /voice Привет, как дела?")
        return

    user_text = ' '.join(context.args)
    processing_msg = await update.message.reply_text("🔊 Генерация голосового ответа...")

    try:
        # 1. Получаем ответ от модели (без отправки текста)
        system_prompt = "Ты эксперт по проекту Венера. Отвечай кратко (до 2 предложений)."
        ai_response = await ask_openrouter(user_text, system_prompt)

        # 2. Синтезируем голос (мужской)
        voice_file = await text_to_speech(ai_response)

        # 3. Отправляем ТОЛЬКО голосовое сообщение
        await context.bot.send_voice(
            chat_id=update.effective_chat.id,
            voice=open(voice_file, 'rb'),
            reply_to_message_id=update.message.message_id
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка генерации: {str(e)}")

    finally:
        if 'voice_file' in locals() and os.path.exists(voice_file):
            os.remove(voice_file)
        if processing_msg:
            await processing_msg.delete()
async def text_to_speech(text: str) -> str:
    """Синтез мужского голоса через edge-tts"""
    filename = f"voice_{uuid.uuid4()}.mp3"
    try:
        communicate = edge_tts.Communicate(
            text=text,
            voice="ru-RU-DmitryNeural",  # Мужской голос
            rate="+10%"  # Слегка ускоряем речь
        )
        await communicate.save(filename)
        return filename
    except Exception as e:
        if os.path.exists(filename):
            os.remove(filename)
        raise RuntimeError(f"Ошибка синтеза голоса: {e}")
async def find_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Укажите описание музыки\nПример: /find грустный джаз для вечера")
        return

    user_request = ' '.join(context.args)
    processing_msg = await update.message.reply_text("🔍 Ищу подходящую музыку...")

    try:
        # 1. Запрашиваем треки у LLM
        tracks = await get_tracks_from_llm(user_request)
        found = False

        # 2. Пробуем каждый трек до первого успешного
        for i, track in enumerate(tracks, 1):
            try:
                await processing_msg.edit_text(
                    f"🔎 Пробую трек {i}/{len(tracks)}: {track}"
                )

                # 3. Пытаемся воспроизвести
                context.args = [track]
                await play_music(update, context)
                found = True
                break

            except Exception as e:
                print(f"Ошибка воспроизведения {track}: {str(e)}")
                continue

        # 4. Если ни один не сработал
        if not found:
            await update.message.reply_text(
                "😢 Не удалось найти ни один из треков\n"
                "Попробуйте другой запрос или уточните параметры"
            )

            # Отправляем список что пробовали (для прозрачности)
            tracks_list = "\n".join(f"• {t}" for t in tracks)
            await update.message.reply_text(
                f"Пробовали найти:\n{tracks_list}"
            )

    except Exception as e:
        await update.message.reply_text(f"❌ Критическая ошибка: {str(e)}")

    finally:
        if processing_msg:
            await processing_msg.delete()
async def get_tracks_from_llm(user_request: str) -> list:
    """Получаем список треков от LLM"""
    prompt = f"""Ты музыкальный эксперт. Пользователь просит: "{user_request}".
Предложи ровно 5 конкретных треков в формате:
1. Исполнитель - Название трека
2. Исполнитель - Название трека
...
Только список, без пояснений!"""

    response = await ask_openrouter(prompt, system_prompt="")

    # Парсим ответ
    tracks = []
    for line in response.split('\n'):
        if '-' in line and any(char.isdigit() for char in line[:3]):
            track = line.split('. ')[-1].strip()
            tracks.append(track)

    if not tracks:
        raise ValueError("Не удалось распознать треки в ответе")

    return tracks[:5]  # Берем первые 5 на случай если LLM вернула больше
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Играть в крестики-нолики",
                              web_app=WebAppInfo(url="https://x0.d0h.ru/"))]
    ]

    await update.message.reply_text(
        "Нажмите кнопку чтобы начать игру:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = json.loads(update.web_app_data.data)
        if data.get('action') == 'share':
            await update.message.reply_text(
                f"Пользователь поделился результатом:\n{data['score']}"
            )
    except Exception as e:
        print(f"WebApp error: {e}")

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
        ("play", play_music), ("p", play_music),
        ("youtube", download_youtube),
        ("twitter", download_twitter),
        ("tiktok", download_tiktok),
        ("vk_playlist", vk_playlist),
        ("say", send_voice_message),
        ("find", find_music),
        ("game", start_game),
        ("vkclip", download_vk_clip)
    ]
    for cmd, handler in commands:
        application.add_handler(CommandHandler(cmd, handler))

    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    application.add_handler(MessageHandler(filters.VOICE, voice_to_text_handler))

    application.run_polling()

if __name__ == "__main__":
    main()
