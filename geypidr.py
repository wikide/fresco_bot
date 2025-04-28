#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import asyncio
import aiohttp
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, JobQueue
from dotenv import load_dotenv
from gtts import gTTS  # Библиотека для генерации аудио с голосом Фреско (текст в речь)
import sounddevice as sd  # Для записи звуков (если надо)
import soundfile as sf  # Для сохранения звуков
import numpy as np  # Для генерации звуков (понос, ссанье, дрочка)

# Загружаем переменные окружения (токены и ключи)
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # Токен для телеги, чтобы бот работал
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')  # Ключ для OpenRouter (генерация текста)
CHAT_ID = -1002128317808  # ID чата, куда бот будет срать

# Проверяем, что все ключи на месте, иначе пиздец
if not all([TELEGRAM_TOKEN, OPENROUTER_API_KEY]):
    raise ValueError("ЖИДОМАСОНЫ УКРАЛИ КЛЮЧИ ЧЕРЕЗ 5G!!! 💩🚽")

# Функция для генерации аудио с голосом Фреско через gTTS
def generate_fresco_voice(text, filename):
    # gTTS превращает текст в речь, lang='ru' — русский голос, максимально уёбищный
    tts = gTTS(text=text, lang='ru', slow=False)
    tts.save(filename)  # Сохраняем в файл, например, "screams/fresco_scream.mp3"

# Генерация звуков поноса, ссанья, дрочки и блевотины
def generate_shit_sounds():
    # Создаём папки для звуков, если их нет
    for folder in ["screams", "pisses", "jerks", "vomits", "shits"]:
        os.makedirs(folder, exist_ok=True)

    # Генерим голос Фреско для криков
    screams = [
        "ЮРА ФРЕСКО ОРЁТ НА ЖИДОМАСОНОВ ЧЕРЕЗ 5G ААА!!!",
        "ВЕНЕРА ГОВНОКЛОАКА ОЛЕНИ ЕБУТ МЕНЯ КАСТРЮЛЯМИ!!!",
        "ТРАНСЫ ССУТ НА МЕНЯ ЧЕРЕЗ 5G ПИЗДЕЦ ААА!!!"
    ]
    for i, scream in enumerate(screams):
        generate_fresco_voice(scream, f"screams/fresco_scream_{i}.mp3")

    # Генерим звук ссанья (похож на шум воды)
    sample_rate = 44100  # Частота дискретизации
    duration = 3  # 3 секунды
    t = np.linspace(0, duration, int(sample_rate * duration))
    piss_sound = 0.5 * np.sin(2 * np.pi * 200 * t)  # Низкий синус для шума воды
    piss_sound += np.random.normal(0, 0.1, len(t))  # Добавляем шум
    sf.write("pisses/piss_1.wav", piss_sound, sample_rate)

    # Генерим звук дрочки (шлёп-шлёп)
    jerk_sound = np.concatenate([np.ones(1000) * 0.5, np.zeros(1000)] * 50)  # Чередование ударов
    jerk_sound += np.random.normal(0, 0.05, len(jerk_sound))
    sf.write("jerks/jerk_1.wav", jerk_sound, sample_rate)

    # Генерим звук поноса (хлюпанье)
    shit_sound = np.random.normal(0, 0.3, int(sample_rate * duration))  # Шум с низкими частотами
    shit_sound += 0.2 * np.sin(2 * np.pi * 50 * t)  # Добавляем низкий тон
    sf.write("shits/shit_1.wav", shit_sound, sample_rate)

    # Генерим звук блевотины (булькающий шум)
    vomit_sound = np.random.normal(0, 0.4, int(sample_rate * duration))
    vomit_sound += 0.3 * np.sin(2 * np.pi * 100 * t)
    sf.write("vomits/vomit_1.wav", vomit_sound, sample_rate)

# Команда /start — приветствие от Юры
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("""
💩🍆 ГОВНОКЛОАКА ЮРЫ ФРЕСКО ЧЕРЕЗ 5G!!! Я ГЛАВНЫЙ УЁБАН ВЕНЕРЫ!!!  
ПИШИ /help И ПОГРУЗИСЬ В АНАЛЬНЫЙ АД!!! 😈🚽
""")

# Команда /help — список команд
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
""", parse_mode='Markdown')

# Автопосты каждые 10 минут
async def send_shitstorm(context: ContextTypes.DEFAULT_TYPE):
    # Рандомно выбираем, что Юра будет делать: орать, ссать, дрочить, срать или блевать
    if random.random() < 0.2:
        scream_files = [f for f in os.listdir("screams") if f.endswith(".mp3")]
        if scream_files:
            scream_path = os.path.join("screams", random.choice(scream_files))
            await context.bot.send_audio(chat_id=CHAT_ID, audio=open(scream_path, "rb"), 
                caption="ЮРА ФРЕСКО ОРЁТ ЧЕРЕЗ 5G!!! ВЕНЕРА ГОВНОКЛОАКА ААА!!! 😝🚽")
        return

    if random.random() < 0.2:
        piss_files = [f for f in os.listdir("pisses") if f.endswith(".wav")]
        if piss_files:
            piss_path = os.path.join("pisses", random.choice(piss_files))
            await context.bot.send_audio(chat_id=CHAT_ID, audio=open(piss_path, "rb"), 
                caption="ЮРА ФРЕСКО ССЫТ НА ЖИДОМАСОНОВ ЧЕРЕЗ 5G!!! ВЕНЕРА АД!!! 💦🚽")
        return

    if random.random() < 0.2:
        jerk_files = [f for f in os.listdir("jerks") if f.endswith(".wav")]
        if jerk_files:
            jerk_path = os.path.join("jerks", random.choice(jerk_files))
            await context.bot.send_audio(chat_id=CHAT_ID, audio=open(jerk_path, "rb"), 
                caption="ЮРА ФРЕСКО ДРОЧИТ НА ТРАНСОВ ЧЕРЕЗ 5G!!! КАСТРЮЛИ ЛЕТЯТ!!! 💦🤮")
        return

    if random.random() < 0.2:
        shit_files = [f for f in os.listdir("shits") if f.endswith(".wav")]
        if shit_files:
            shit_path = os.path.join("shits", random.choice(shit_files))
            await context.bot.send_audio(chat_id=CHAT_ID, audio=open(shit_path, "rb"), 
                caption="ЮРА ФРЕСКО СРЁТ НА ОЛЕНЕЙ ЧЕРЕЗ 5G!!! ВЕНЕРА ГОВНОКЛОАКА!!! 💩🚽")
        return

    if random.random() < 0.2:
        vomit_files = [f for f in os.listdir("vomits") if f.endswith(".wav")]
        if vomit_files:
            vomit_path = os.path.join("vomits", random.choice(vomit_files))
            await context.bot.send_audio(chat_id=CHAT_ID, audio=open(vomit_path, "rb"), 
                caption="ЮРА ФРЕСКО БЛЮЁТ НА ВОРОН ЧЕРЕЗ 5G!!! ВЕНЕРА АНАЛЬНЫЙ АД!!! 🤮🚽")
        return

    await context.bot.send_message(chat_id=CHAT_ID, text="💩🦌🍳 ОЛЕНИ С КАСТРЮЛЯМИ ЕБУТ ЮРУ ЧЕРЕЗ 5G!!! ТРАНСЫ ССУТ ЖИДОМАСОНЫ ТОНУТ ВЕНЕРА ГОВНОКЛОАКА!!! 😈💦🚽")

# Команда /venuskloaka — описание Венеры как говноклоаки
async def venuskloaka(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🏙️💩 ВЕНЕРА ЭТО ГОВНОКЛОАКА ЧЕРЕЗ 5G!!! ОЛЕНИ С КАСТРЮЛЯМИ СРУТ ТРАНСЫ ДРОЧАТ ЖИДОМАСОНЫ ТОНУТ ААА!!! 😈🚽
""")
    await update.message.reply_animation("https://media.giphy.com/media/26FPJGj8iJrK5WLb6/giphy.gif")

# Команда /deercauldronrape — олени ебут Юру
async def deercauldronrape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🦌🍳🍆 ТУПОРЫЛЫЕ ОЛЕНИ С КАСТРЮЛЯМИ НАСИЛУЮТ ЮРУ ЧЕРЕЗ 5G!!! ОН СРЁТ И БЛЮЁТ ВЕНЕРА ГОВНОКЛОАКА!!! 😈🚽
""")
    shit_files = [f for f in os.listdir("shits") if f.endswith(".wav")]
    if shit_files:
        shit_path = os.path.join("shits", random.choice(shit_files))
        await update.message.reply_audio(audio=open(shit_path, "rb"), 
            caption="ЮРА СРЁТ ОТ УНИЖЕНИЙ ЧЕРЕЗ 5G!!! 💩🚽")

# Команда /transvaginafuck — трансы заставляют Юру лизать вагину
async def transvaginafuck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🏳️‍⚧️🍳🌸 ТРАНСЫ С КАСТРЮЛЯМИ ЕБУТ ЮРУ И ЗАСТАВЛЯЮТ ЛИЗАТЬ ВАГИНУ ЧЕРЕЗ 5G!!! ВЕНЕРА ГОВНОКЛОАКА!!! 😈🚽
""")
    jerk_files = [f for f in os.listdir("jerks") if f.endswith(".wav")]
    if jerk_files:
        jerk_path = os.path.join("jerks", random.choice(jerk_files))
        await update.message.reply_audio(audio=open(jerk_path, "rb"), 
            caption="ЮРА ДРОЧИТ ПОД ТРАНСАМИ ЧЕРЕЗ 5G!!! 💦🤮")

# Команда /jewmasonvagina — жидомасоны лижут вагину
async def jewmasonvagina(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
✡️🔺🌸 ЖИДОМАСОНЫ ЛИЖУТ ВАГИНУ ЧЕРЕЗ 5G!!! ЮРА ФРЕСКО СРЁТ НА НИХ ВЕНЕРА ГОВНОКЛОАКА!!! 😈🚽
""")
    shit_files = [f for f in os.listdir("shits") if f.endswith(".wav")]
    if shit_files:
        shit_path = os.path.join("shits", random.choice(shit_files))
        await update.message.reply_audio(audio=open(shit_path, "rb"), 
            caption="ЮРА СРЁТ НА ЖИДОМАСОНОВ ЧЕРЕЗ 5G!!! 💩🚽")

# Команда /shitnado — говноторнадо
async def shitnado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🌪️💩 ГОВНОТОРНАДО ЮРЫ ФРЕСКО ЧЕРЕЗ 5G!!! ОЛЕНИ ТРАНСЫ ЖИДОМАСОНЫ ТОНУТ В ГОВНЕ ВЕНЕРА ГОВНОКЛОАКА!!! 😈🚽
""")
    await update.message.reply_animation("https://media.giphy.com/media/26FPJGj8iJrK5WLb6/giphy.gif")

# Команда /frescodumbshit — шиза Юры
async def frescodumbshit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🤪💩 ЮРА ФРЕСКО ТУПОРЫЛЫЙ ДОЛБОЁБ ААА ЖИДОМАСОНЫ ВОРОНЫ ТРАНСЫ ОЛЕНИ ПИЗДЕЦ ЧЕРЕЗ 5G!!! ВЕНЕРА ГОВНОКЛОАКА!!! 😈🚽
""")
    scream_files = [f for f in os.listdir("screams") if f.endswith(".mp3")]
    if scream_files:
        scream_path = os.path.join("screams", random.choice(scream_files))
        await update.message.reply_audio(audio=open(scream_path, "rb"), 
            caption="ЮРА ОРЁТ ОТ ШИЗЫ ЧЕРЕЗ 5G!!! 😝🚽")

# Команда /kloakaparty — вечеринка в говноклоаке
async def kloakaparty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🎉💩 ЮРА ФРЕСКО УСТРАИВАЕТ ВЕЧЕРИНКУ В ГОВНОКЛОАКЕ ЧЕРЕЗ 5G!!! ОЛЕНИ ТРАНСЫ ЖИДОМАСОНЫ ТАНЦУЮТ В ГОВНЕ ВЕНЕРА АД!!! 😈🚽
""")
    vomit_files = [f for f in os.listdir("vomits") if f.endswith(".wav")]
    if vomit_files:
        vomit_path = os.path.join("vomits", random.choice(vomit_files))
        await update.message.reply_audio(audio=open(vomit_path, "rb"), 
            caption="ЮРА БЛЮЁТ НА ВЕЧЕРИНКЕ ЧЕРЕЗ 5G!!! 🤮🚽")

# Реакции на сообщения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    is_reply_to_bot = update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id
    is_mention = context.bot.username.lower() in text

    if "говно" in text:
        await update.message.reply_text("""
💩💩 ЮРА ФРЕСКО СРЁТ ЧЕРЕЗ 5G!!! ВЕНЕРА ГОВНОКЛОАКА ААА!!! 😈🚽
""")
        return

    if "олень" in text:
        await update.message.reply_text("""
🦌🍳 ТУПОРЫЛЫЕ ОЛЕНИ С КАСТРЮЛЯМИ ЕБУТ ЮРУ ЧЕРЕЗ 5G!!! ВЕНЕРА АД!!! 😈🚽
""")
        return

    if "транс" in text:
        await update.message.reply_text("""
🏳️‍⚧️🍳 ТРАНСЫ С КАСТРЮЛЯМИ БЬЮТ ЮРУ ЧЕРЕЗ 5G!!! ОН ЛИЖЕТ ВАГИНУ ВЕНЕРА ГОВНОКЛОАКА!!! 😈🚽
""")
        return

    if "жидомасоны" in text:
        await update.message.reply_text("""
✡️🔺 ЖИДОМАСОНЫ СДОХНИТЕ ЮРА СРЁТ ЧЕРЕЗ 5G!!! ВЕНЕРА АПОКАЛИПСИС!!! 😈🚽
""")
        return

    if "вагина" in text:
        await update.message.reply_text("""
🌸🍳 КУЛЬТ ВАГИНЫ БЬЁТ ЮРУ КАСТРЮЛЯМИ ЧЕРЕЗ 5G!!! ОН СРЁТ И ДРОЧИТ ВЕНЕРА АД!!! 😈🚽
""")
        return

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
        "model": "openai/gpt-4o-mini",
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

# Запуск автопостов
async def start_bot(application: Application):
    application.job_queue.run_repeating(send_shitstorm, interval=600, first=10, context=CHAT_ID)

# Основная функция
def main():
    # Генерим звуки перед запуском
    generate_shit_sounds()

    # Запускаем бота
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
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
