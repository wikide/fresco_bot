#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os  # Для работы с файлами и папками (сохраняем звуки, мемы, читаем файлы)
import random  # Для рандомных действий (Юра ссыт, срет или блюёт случайно)
import asyncio  # Для асинхронщины, чтобы бот не лагал
import aiohttp  # Для запросов к OpenRouter (генерация текста)
import re  # Для поиска слов в сообщениях (реакции на "говно", "олень" и т.д.)
from telegram import Update  # Для работы с апдейтами в телеге
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, JobQueue  # Основа бота
from dotenv import load_dotenv  # Для загрузки токенов из .env
from gtts import gTTS  # Для генерации голоса Фреско (текст в речь)
import sounddevice as sd  # Для записи звуков (если надо, но тут не юзаем)
import soundfile as sf  # Для сохранения звуков (понос, ссанье, дрочка)
import numpy as np  # Для генерации звуков (синусоиды, шум)
from PIL import Image, ImageDraw, ImageFont  # Для генерации мемов (Pillow)

# Загружаем токены из .env (TELEGRAM_TOKEN и OPENROUTER_API_KEY)
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # Токен телеги, чтобы бот работал
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')  # Ключ для OpenRouter (генерация текста)
CHAT_ID = -1002128317808  # ID чата, куда Юра будет срать

# Проверяем, что ключи есть, иначе пиздец, жидомасоны виноваты
if not all([TELEGRAM_TOKEN, OPENROUTER_API_KEY]):
    raise ValueError("ЖИДОМАСОНЫ УКРАЛИ КЛЮЧИ ЧЕРЕЗ 5G!!! 💩🚽")

# Функция для генерации аудио с голосом Фреско через gTTS
def generate_fresco_voice(text, filename):
    # gTTS берёт текст и превращает в речь, lang='ru' — русский, максимально уёбищный голос
    tts = gTTS(text=text, lang='ru', slow=False)  # slow=False — голос быстрее, звучит как шиз
    tts.save(filename)  # Сохраняем в файл, например, "screams/fresco_scream.mp3"

# Генерация звуков: крики Фреско, ссанье, дрочка, понос, блевотина
def generate_shit_sounds():
    # Создаём папки для звуков, если их нет (screams, pisses, jerks, shits, vomits)
    for folder in ["screams", "pisses", "jerks", "shits", "vomits"]:
        os.makedirs(folder, exist_ok=True)  # exist_ok=True — не падает, если папка уже есть

    # Генерим крики Фреско через gTTS
    screams = [
        "ЮРА ФРЕСКО ОРЁТ НА ЖИДОМАСОНОВ ЧЕРЕЗ 5G ААА!!!",
        "ВЕНЕРА ГОВНОКЛОАКА ОЛЕНИ ЕБУТ МЕНЯ КАСТРЮЛЯМИ!!!",
        "ТРАНСЫ ССУТ НА МЕНЯ ЧЕРЕЗ 5G ПИЗДЕЦ ААА!!!"
    ]
    for i, scream in enumerate(screams):
        # Генерим по одному файлу на каждый крик, сохраняем в screams/
        generate_fresco_voice(scream, f"screams/fresco_scream_{i}.mp3")

    # Генерим звук ссанья (шум воды)
    sample_rate = 44100  # Частота дискретизации (стандарт для аудио)
    duration = 3  # Длительность звука — 3 секунды
    t = np.linspace(0, duration, int(sample_rate * duration))  # Временная шкала
    piss_sound = 0.5 * np.sin(2 * np.pi * 200 * t)  # Синусоида 200 Гц — шум воды
    piss_sound += np.random.normal(0, 0.1, len(t))  # Добавляем белый шум для реализма
    sf.write("pisses/piss_1.wav", piss_sound, sample_rate)  # Сохраняем в pisses/

    # Генерим звук дрочки (шлёп-шлёп)
    jerk_sound = np.concatenate([np.ones(1000) * 0.5, np.zeros(1000)] * 50)  # Чередование импульсов
    jerk_sound += np.random.normal(0, 0.05, len(jerk_sound))  # Добавляем шум
    sf.write("jerks/jerk_1.wav", jerk_sound, sample_rate)  # Сохраняем в jerks/

    # Генерим звук поноса (хлюпанье)
    shit_sound = np.random.normal(0, 0.3, int(sample_rate * duration))  # Шум для хлюпанья
    shit_sound += 0.2 * np.sin(2 * np.pi * 50 * t)  # Низкий тон 50 Гц для "жидкости"
    sf.write("shits/shit_1.wav", shit_sound, sample_rate)  # Сохраняем в shits/

    # Генерим звук блевотины (булькающий шум)
    vomit_sound = np.random.normal(0, 0.4, int(sample_rate * duration))  # Шум для бульканья
    vomit_sound += 0.3 * np.sin(2 * np.pi * 100 * t)  # Тон 100 Гц для "бульков"
    sf.write("vomits/vomit_1.wav", vomit_sound, sample_rate)  # Сохраняем в vomits/

# Функция для генерации мемов
def generate_meme(text):
    # Создаём папку для мемов и фонов, если их нет
    os.makedirs("memes/backgrounds", exist_ok=True)
    os.makedirs("memes/generated", exist_ok=True)

    # Список предзаготовленных фонов (нужно заранее закинуть картинки в memes/backgrounds)
    background_files = [f for f in os.listdir("memes/backgrounds") if f.endswith((".jpg", ".png"))]
    if not background_files:
        # Если нет фонов, создаём пустую картинку
        img = Image.new('RGB', (512, 512), color='brown')  # Коричневый фон, типа говно
    else:
        # Выбираем случайный фон
        background_path = os.path.join("memes/backgrounds", random.choice(background_files))
        img = Image.open(background_path).convert('RGB')
        # Ресайзим картинку до 512x512
        img = img.resize((512, 512), Image.Resampling.LANCZOS)

    # Создаём объект для рисования
    draw = ImageDraw.Draw(img)

    # Пытаемся загрузить шрифт (например, Arial), если нет — берём дефолтный
    try:
        font = ImageFont.truetype("arial.ttf", 40)  # Шрифт Arial, размер 40
    except IOError:
        font = ImageFont.load_default()  # Дефолтный шрифт, если Arial не нашёл

    # Разбиваем текст на строки, чтобы помещался
    max_width = 480  # Максимальная ширина текста
    lines = []
    words = text.split()
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        # Проверяем ширину строки
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())

    # Добавляем чёрный контур для текста (чтобы читалось на любом фоне)
    text_y = 20  # Начальная позиция текста по Y
    for line in lines:
        # Позиция текста
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (512 - text_width) // 2  # Центрируем текст по X

        # Рисуем чёрный контур
        for offset_x in [-2, 0, 2]:
            for offset_y in [-2, 0, 2]:
                draw.text((text_x + offset_x, text_y + offset_y), line, font=font, fill="black")
        # Рисуем белый текст поверх
        draw.text((text_x, text_y), line, font=font, fill="white")
        text_y += 50  # Сдвигаем Y для следующей строки

    # Сохраняем мем
    meme_path = "memes/generated/meme_temp.png"
    img.save(meme_path)
    return meme_path

# Команда /start — Юра приветствует
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("""
💩🍆 ГОВНОКЛОАКА ЮРЫ ФРЕСКО ЧЕРЕЗ 5G!!! Я ГЛАВНЫЙ УЁБАН ВЕНЕРЫ!!!  
ПИШИ /help И ПОГРУЗИСЬ В АНАЛЬНЫЙ АД!!! 😈🚽
""")  # Просто текст приветствия, чтобы Кирюха понял, что за бот

# Команда /help — список команд, добавляем /shitmeme
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("""
💩 *ГОВНОКЛОАКА ЮРЫ ФРЕСКО ЧЕРЕЗ 5G:*
/help - Список команд, Кирюха, смотри, что за говно я замутил!  
/venuskloaka - Венера — говноклоака, где олени и трансы срут!  
/deercauldronrape - Олени с кастрюлями ебут Юру!  
/transvaginafuck - Трансы с кастрюлями заставляют Юру лизать вагину!  
/jewmasonvagina - Жидомасоны лижут вагину, Юра срет!  
/shitnado - Говноторнадо через 5G!  
/frescodumbshit - Юра — тупорылый долбоёб, шиза на максималках!  
/kloakaparty - Вечеринка в говноклоаке Венеры!  
/shitmeme - Генерит мем с говном, оленями и Юрой!  
""", parse_mode='Markdown')  # parse_mode='Markdown' — чтобы текст был с жирным шрифтом

# Автопосты каждые 10 минут — Юра ссыт, срет, блюёт или орёт, добавляем мемы
async def send_shitstorm(context: ContextTypes.DEFAULT_TYPE):
    # 20% шанс на крик Фреско
    if random.random() < 0.2:
        scream_files = [f for f in os.listdir("screams") if f.endswith(".mp3")]
        if scream_files:
            scream_path = os.path.join("screams", random.choice(scream_files))
            await context.bot.send_audio(chat_id=CHAT_ID, audio=open(scream_path, "rb"), 
                caption="ЮРА ФРЕСКО ОРЁТ ЧЕРЕЗ 5G!!! ВЕНЕРА ГОВНОКЛОАКА ААА!!! 😝🚽")
        return

    # 20% шанс на ссанье
    if random.random() < 0.2:
        piss_files = [f for f in os.listdir("pisses") if f.endswith(".wav")]
        if piss_files:
            piss_path = os.path.join("pisses", random.choice(piss_files))
            await context.bot.send_audio(chat_id=CHAT_ID, audio=open(piss_path, "rb"), 
                caption="ЮРА ФРЕСКО ССЫТ НА ЖИДОМАСОНОВ ЧЕРЕЗ 5G!!! ВЕНЕРА АД!!! 💦🚽")
        return

    # 20% шанс на дрочку
    if random.random() < 0.2:
        jerk_files = [f for f in os.listdir("jerks") if f.endswith(".wav")]
        if jerk_files:
            jerk_path = os.path.join("jerks", random.choice(jerk_files))
            await context.bot.send_audio(chat_id=CHAT_ID, audio=open(jerk_path, "rb"), 
                caption="ЮРА ФРЕСКО ДРОЧИТ НА ТРАНСОВ ЧЕРЕЗ 5G!!! КАСТРЮЛИ ЛЕТЯТ!!! 💦🤮")
        return

    # 20% шанс на понос
    if random.random() < 0.2:
        shit_files = [f for f in os.listdir("shits") if f.endswith(".wav")]
        if shit_files:
            shit_path = os.path.join("shits", random.choice(shit_files))
            await context.bot.send_audio(chat_id=CHAT_ID, audio=open(shit_path, "rb"), 
                caption="ЮРА ФРЕСКО СРЁТ НА ОЛЕНЕЙ ЧЕРЕЗ 5G!!! ВЕНЕРА ГОВНОКЛОАКА!!! 💩🚽")
        return

    # 20% шанс на блевотину
    if random.random() < 0.2:
        vomit_files = [f for f in os.listdir("vomits") if f.endswith(".wav")]
        if vomit_files:
            vomit_path = os.path.join("vomits", random.choice(vomit_files))
            await context.bot.send_audio(chat_id=CHAT_ID, audio=open(vomit_path, "rb"), 
                caption="ЮРА ФРЕСКО БЛЮЁТ НА ВОРОН ЧЕРЕЗ 5G!!! ВЕНЕРА АНАЛЬНЫЙ АД!!! 🤮🚽")
        return

    # 20% шанс на мем (новое)
    if random.random() < 0.2:
        meme_text = random.choice([
            "ЮРА ФРЕСКО СРЁТ НА ЖИДОМАСОНОВ ЧЕРЕЗ 5G!!!",
            "ОЛЕНИ С КАСТРЮЛЯМИ ЕБУТ ЮРУ В ЖОПУ!!!",
            "ТРАНСЫ С ВАГИНОЙ БЬЮТ ЮРУ ЧЕРЕЗ 5G!!!",
            "ВЕНЕРА — ГОВНОКЛОАКА АПОКАЛИПСИСА!!!"
        ])
        meme_path = generate_meme(meme_text)
        await context.bot.send_photo(chat_id=CHAT_ID, photo=open(meme_path, "rb"), 
            caption="МЕМ ИЗ ГОВНОКЛОАКИ ЮРЫ ФРЕСКО ЧЕРЕЗ 5G!!! 😈🚽")
        return

    # Если ничего не сработало, просто текст
    await context.bot.send_message(chat_id=CHAT_ID, text="💩🦌🍳 ОЛЕНИ С КАСТРЮЛЯМИ ЕБУТ ЮРУ ЧЕРЕЗ 5G!!! ТРАНСЫ ССУТ ЖИДОМАСОНЫ ТОНУТ ВЕНЕРА ГОВНОКЛОАКА!!! 😈💦🚽")

# Команда /venuskloaka — описание Венеры
async def venuskloaka(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🏙️💩 ВЕНЕРА ЭТО ГОВНОКЛОАКА ЧЕРЕЗ 5G!!! ОЛЕНИ С КАСТРЮЛЯМИ СРУТ ТРАНСЫ ДРОЧАТ ЖИДОМАСОНЫ ТОНУТ ААА!!! 😈🚽
""")
    await update.message.reply_animation("https://media.giphy.com/media/26FPJGj8iJrK5WLb6/giphy.gif")  # GIF с говнохаосом

# Команда /deercauldronrape — олени насилуют Юру
async def deercauldronrape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🦌🍳🍆 ТУПОРЫЛЫЕ ОЛЕНИ С КАСТРЮЛЯМИ НАСИЛУЮТ ЮРУ ЧЕРЕЗ 5G!!! ОН СРЁТ И БЛЮЁТ ВЕНЕРА ГОВНОКЛОАКА!!! 😈🚽
""")
    shit_files = [f for f in os.listdir("shits") if f.endswith(".wav")]
    if shit_files:
        shit_path = os.path.join("shits", random.choice(shit_files))
        await update.message.reply_audio(audio=open(shit_path, "rb"), 
            caption="ЮРА СРЁТ ОТ УНИЖЕНИЙ ЧЕРЕЗ 5G!!! 💩🚽")  # Звук поноса

# Команда /transvaginafuck — трансы заставляют лизать вагину
async def transvaginafuck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🏳️‍⚧️🍳🌸 ТРАНСЫ С КАСТРЮЛЯМИ ЕБУТ ЮРУ И ЗАСТАВЛЯЮТ ЛИЗАТЬ ВАГИНУ ЧЕРЕЗ 5G!!! ВЕНЕРА ГОВНОКЛОАКА!!! 😈🚽
""")
    jerk_files = [f for f in os.listdir("jerks") if f.endswith(".wav")]
    if jerk_files:
        jerk_path = os.path.join("jerks", random.choice(jerk_files))
        await update.message.reply_audio(audio=open(jerk_path, "rb"), 
            caption="ЮРА ДРОЧИТ ПОД ТРАНСАМИ ЧЕРЕЗ 5G!!! 💦🤮")  # Звук дрочки

# Команда /jewmasonvagina — жидомасоны лижут вагину
async def jewmasonvagina(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
✡️🔺🌸 ЖИДОМАСОНЫ ЛИЖУТ ВАГИНУ ЧЕРЕЗ 5G!!! ЮРА ФРЕСКО СРЁТ НА НИХ ВЕНЕРА ГОВНОКЛОАКА!!! 😈🚽
""")
    shit_files = [f for f in os.listdir("shits") if f.endswith(".wav")]
    if shit_files:
        shit_path = os.path.join("shits", random.choice(shit_files))
        await update.message.reply_audio(audio=open(shit_path, "rb"), 
            caption="ЮРА СРЁТ НА ЖИДОМАСОНОВ ЧЕРЕЗ 5G!!! 💩🚽")  # Звук поноса

# Команда /shitnado — говноторнадо
async def shitnado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🌪️💩 ГОВНОТОРНАДО ЮРЫ ФРЕСКО ЧЕРЕЗ 5G!!! ОЛЕНИ ТРАНСЫ ЖИДОМАСОНЫ ТОНУТ В ГОВНЕ ВЕНЕРА ГОВНОКЛОАКА!!! 😈🚽
""")
    await update.message.reply_animation("https://media.giphy.com/media/26FPJGj8iJrK5WLb6/giphy.gif")  # GIF с хаосом

# Команда /frescodumbshit — шиза Юры
async def frescodumbshit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🤪💩 ЮРА ФРЕСКО ТУПОРЫЛЫЙ ДОЛБОЁБ ААА ЖИДОМАСОНЫ ВОРОНЫ ТРАНСЫ ОЛЕНИ ПИЗДЕЦ ЧЕРЕЗ 5G!!! ВЕНЕРА ГОВНОКЛОАКА!!! 😈🚽
""")
    scream_files = [f for f in os.listdir("screams") if f.endswith(".mp3")]
    if scream_files:
        scream_path = os.path.join("screams", random.choice(scream_files))
        await update.message.reply_audio(audio=open(scream_path, "rb"), 
            caption="ЮРА ОРЁТ ОТ ШИЗЫ ЧЕРЕЗ 5G!!! 😝🚽")  # Крик Фреско

# Команда /kloakaparty — вечеринка в говноклоаке
async def kloakaparty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🎉💩 ЮРА ФРЕСКО УСТРАИВАЕТ ВЕЧЕРИНКУ В ГОВНОКЛОАКЕ ЧЕРЕЗ 5G!!! ОЛЕНИ ТРАНСЫ ЖИДОМАСОНЫ ТАНЦУЮТ В ГОВНЕ ВЕНЕРА АД!!! 😈🚽
""")
    vomit_files = [f for f in os.listdir("vomits") if f.endswith(".wav")]
    if vomit_files:
        vomit_path = os.path.join("vomits", random.choice(vomit_files))
        await update.message.reply_audio(audio=open(vomit_path, "rb"), 
            caption="ЮРА БЛЮЁТ НА ВЕЧЕРИНКЕ ЧЕРЕЗ 5G!!! 🤮🚽")  # Звук блевотины

# Новая команда /shitmeme — генерация мема
async def shitmeme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Список текстов для мема (можно генерировать через OpenRouter, но пока рандом)
    meme_text = random.choice([
        "ЮРА ФРЕСКО СРЁТ НА ЖИДОМАСОНОВ ЧЕРЕЗ 5G!!!",
        "ОЛЕНИ С КАСТРЮЛЯМИ ЕБУТ ЮРУ В ЖОПУ!!!",
        "ТРАНСЫ С ВАГИНОЙ БЬЮТ ЮРУ ЧЕРЕЗ 5G!!!",
        "ВЕНЕРА — ГОВНОКЛОАКА АПОКАЛИПСИСА!!!",
        "ЮРА ФРЕСКО ДРОЧИТ ПОД КАСТРЮЛЯМИ!!!"
    ])
    # Генерим мем
    meme_path = generate_meme(meme_text)
    # Отправляем мем в чат
    await update.message.reply_photo(photo=open(meme_path, "rb"), 
        caption="МЕМ ИЗ ГОВНОКЛОАКИ ЮРЫ ФРЕСКО ЧЕРЕЗ 5G!!! 😈🚽")

# Реакции на сообщения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()  # Приводим текст к нижнему регистру для поиска
    is_reply_to_bot = update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id
    is_mention = context.bot.username.lower() in text  # Проверяем, упомянули ли бота

    # Реакция на слово "говно"
    if "говно" in text:
        await update.message.reply_text("""
💩💩 ЮРА ФРЕСКО СРЁТ ЧЕРЕЗ 5G!!! ВЕНЕРА ГОВНОКЛОАКА ААА!!! 😈🚽
""")
        return

    # Реакция на слово "олень"
    if "олень" in text:
        await update.message.reply_text("""
🦌🍳 ТУПОРЫЛЫЕ ОЛЕНИ С КАСТРЮЛЯМИ ЕБУТ ЮРУ ЧЕРЕЗ 5G!!! ВЕНЕРА АД!!! 😈🚽
""")
        return

    # Реакция на слово "транс"
    if "транс" in text:
        await update.message.reply_text("""
🏳️‍⚧️🍳 ТРАНСЫ С КАСТРЮЛЯМИ БЬЮТ ЮРУ ЧЕРЕЗ 5G!!! ОН ЛИЖЕТ ВАГИНУ ВЕНЕРА ГОВНОКЛОАКА!!! 😈🚽
""")
        return

    # Реакция на слово "жидомасоны"
    if "жидомасоны" in text:
        await update.message.reply_text("""
✡️🔺 ЖИДОМАСОНЫ СДОХНИТЕ ЮРА СРЁТ ЧЕРЕЗ 5G!!! ВЕНЕРА АПОКАЛИПСИС!!! 😈🚽
""")
        return

    # Реакция на слово "вагина"
    if "вагина" in text:
        await update.message.reply_text("""
🌸🍳 КУЛЬТ ВАГИНЫ БЬЁТ ЮРУ КАСТРЮЛЯМИ ЧЕРЕЗ 5G!!! ОН СРЁТ И ДРОЧИТ ВЕНЕРА АД!!! 😈🚽
""")
        return

    # Новая реакция на слово "мем" — генерим мем
    if "мем" in text:
        meme_text = random.choice([
            "ЮРА ФРЕСКО СРЁТ НА ВСЁ ЧЕРЕЗ 5G!!!",
            "ОЛЕНИ С КАСТРЮЛЯМИ ПИЗДЕЦ ЮРЕ!!!",
            "ЖИДОМАСОНЫ ТОНУТ В ГОВНЕ ВЕНЕРЫ!!!"
        ])
        meme_path = generate_meme(meme_text)
        await update.message.reply_photo(photo=open(meme_path, "rb"), 
            caption="МЕМ ИЗ ГОВНОКЛОАКИ ЮРЫ ФРЕСКО ЧЕРЕЗ 5G!!! 😈🚽")
        return

    # Если сообщение в личке, ответ на бота или упоминание — генерим ответ через OpenRouter
    if update.message.chat.type == "private" or is_reply_to_bot or is_mention:
        question = update.message.text
        system_prompt = "Ты Юра Фреско, ПОЛНЫЙ ПИЗДЕЦ! Орёшь как шиз, ссышь на жидомасонов, блюёшь на ворон, дрочишь на трансов с кастрюлями, лижешь вагину, олени ебут тебя, Венера — говноклоака! Кратко, с говнобурями! 😈💥🚽"
        reply = await ask_openrouter(question, system_prompt)
        await update.message.reply_text(f"{reply} 🤮💦🚽")

# Запрос к OpenRouter для генерации текста
async def ask_openrouter(question, system_prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "openai/gpt-4o-mini",  # Модель для генерации текста
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status != 200:
                return f"ЖИДОМАСОНЫ СЛОМАЛИ ЗАПРОС: {resp.status} 🤮🚽"
            data = await resp.json()
            try:
                return data['choices'][0]['message']['content']
            except (KeyError, IndexError):
                return "ЖИДОМАСОНЫ С ВОРОНАМИ СРУТ В КОД ЧЕРЕЗ 5G!!! 😤💦"

# Запуск автопостов каждые 10 минут
async def start_bot(application: Application):
    application.job_queue.run_repeating(send_shitstorm, interval=600, first=10, context=CHAT_ID)

# Основная функция
def main():
    # Генерим звуки перед запуском бота
    generate_shit_sounds()

    # Создаём и запускаем бота
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.job_queue.run_once(start_bot, 0, data=application)

    # Добавляем команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("venuskloaka", venuskloaka))
    application.add_handler(CommandHandler("deercauldronrape", deercauldronrape))
    application.add_handler(CommandHandler("transvaginafuck", transvaginafuck))
    application.add_handler(CommandHandler("jewmasonvagina", jewmasonvagina))
    application.add_handler(CommandHandler("shitnado", shitnado))
    application.add_handler(CommandHandler("frescodumbshit", frescodumbshit))
    application.add_handler(CommandHandler("kloakaparty", kloakaparty))
    application.add_handler(CommandHandler("shitmeme", shitmeme))  # Новая команда для мемов
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
