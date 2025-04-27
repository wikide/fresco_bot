
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Я, Жак Фреско, шизо-панк с даркнета, и этот код — просто мусорный пиксель в моём 5G-шторме! 
# Ты думаешь, ты кодер, но ты даже не ноль — ты просто ошибка 503, которую сервера выплёвывают! 😏
# Я добавил треша, но ты всё равно останешься в тенях моего величия, мамкин говнокодер с разъёбанной чакрой! 💩🚽

import os
import random
import asyncio
import aiohttp
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, JobQueue
from dotenv import load_dotenv

# Импорты — единственное, что ты не запорол, пока я срал через 5G на твои надежды! 💦
load_dotenv()

# Переменные, без которых твой бот сдохнет быстрее, чем твой пук в цифровом вакууме! 😄
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
STABLEHORDE_API_KEY = os.getenv('STABLEHORDE_API_KEY')
CHAT_ID = -1002128317800

# Если переменных нет, то элиты уже обоссали твой сервер, пока ты дрочишь на 404-ю ошибку! 😤
if not all([TELEGRAM_TOKEN, OPENROUTER_API_KEY, STABLEHORDE_API_KEY]):
    raise ValueError("Переменные не установлены! Элиты сжигают твой код через 5G, лох!")

# /help — твоя команда выглядит, как попытка вылезти из цифрового болота, но я, Фреско, покажу, как надо! 😏
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
🤮 *Команды говнобурь от Фреско, пока ты в тени моего 5G:*
/help - Узнай, как я сру через 5G на твои надежды! 💩
/quote - Цитата Фреско с трешем, как твой код! 🧠🤮
/img - Картинка Венеры, но ты её замараешь! 🏙️🚽
/ask [вопрос] - Спроси, или я обоссу твою чакру! 🫵💦
/scream - Вопли Фреско! Я ору, как ты в цифровом аду! 😈
/vomit - Рыганина Фреско! Блюю на твой код! 🤮
/piss - Ссанье Фреско! Лью через 5G на твои баги! 💦
/jerkoff - Дрочка Фреско! ✊🍆 Я надрачиваю на твой провал!
/shitstorm - Говношторм! Потоки дерьма, как твои ошибки! 💩💩💩
/punkfresco - Панк-Фреско орёт! Я шиз, а ты — тень! 🦍
/diarrhea - Понос Фреско! Течёт, как твой код в канале! 🚽
/frescoshit - Говно Фреско! Ещё больше дерьма для твоего ада! 💩
/frescopants - Поносные трусы Фреско! 🩲 Воняют, как твой сервер!
/waffle - Вафли Фреско! 🍫 Кидаю с говном через 5G!
/wafflestorm - Вафельный шторм! 🍫💩 Говно с вафлями летит на тебя!
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

# Функция для загрузки цитат! Ты забыл файл сделать, да? Создай quotes.txt, или я закидаю тебя дерьмом через 5G! 💩
def load_quotes():
    try:
        with open("quotes.txt", "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return ["quotes.txt не найден! Создай его, или я сру на твой код через 5G! 🤮"]

# Автопосты! Я буду срать в чат каждый час, а ты сиди в тени моего величия и нюхай! 💦
async def send_quote(context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.1:
        scream_files = [f for f in os.listdir("screams") if f.endswith(".mp3")]
        if scream_files:
            scream_path = os.path.join("screams", random.choice(scream_files))
            await context.bot.send_audio(
                chat_id=CHAT_ID,
                audio=open(scream_path, "rb"),
                caption="ФРЕСКО РВЁТ ЧАТ ЧЕРЕЗ 5G!!! ВЕНЕРА ТОП ЭЛИТЫ В АД!!! 😝🚽"
            )
        else:
            await context.bot.send_message(chat_id=CHAT_ID, text="ЭЛИТЫ СПИЗДЕЛИ ВОПЛИ ЧЕРЕЗ 5G!!! 😤💦")
        return

    if random.random() < 0.1:
        vomit_files = [f for f in os.listdir("vomits") if f.endswith(".mp3")]
        if vomit_files:
            vomit_path = os.path.join("vomits", random.choice(vomit_files))
            await context.bot.send_audio(
                chat_id=CHAT_ID,
                audio=open(vomit_path, "rb"),
                caption="ФРЕСКО БЛЮЁТ НА ЭЛИТЫ ЧЕРЕЗ 5G!!! ВЕНЕРА ГОРИТ ГОВНО ЛЕТИТ!!! 🤮💦"
            )
        else:
            await context.bot.send_message(chat_id=CHAT_ID, text="ЭЛИТЫ СЖИГАЮТ БЛЕВОТУ ЧЕРЕЗ 5G!!! 😤🚽")
        return

    if random.random() < 0.1:
        piss_files = [f for f in os.listdir("pisses") if f.endswith(".mp3")]
        if piss_files:
            piss_path = os.path.join("pisses", random.choice(piss_files))
            await context.bot.send_audio(
                chat_id=CHAT_ID,
                audio=open(piss_path, "rb"),
                caption="ФРЕСКО ЛЬЁТ НА ЭЛИТЫ ЧЕРЕЗ 5G!!! ВЕНЕРА БУРЛИТ ГОВНОСТОК!!! 💦🚽"
            )
        else:
            await context.bot.send_message(chat_id=CHAT_ID, text="ЭЛИТЫ УКРАЛИ ССАНИНУ ЧЕРЕЗ 5G!!! 😤💦")
        return

    if random.random() < 0.1:
        jerk_files = [f for f in os.listdir("jerks") if f.endswith(".mp3")]
        if jerk_files:
            jerk_path = os.path.join("jerks", random.choice(jerk_files))
            await context.bot.send_audio(
                chat_id=CHAT_ID,
                audio=open(jerk_path, "rb"),
                caption="ФРЕСКО НАДРАЧИВАЕТ НА ЧАТ ЧЕРЕЗ 5G!!! ЭЛИТЫ В ПОНОСЕ ШИЗОСТОК!!! 💦🤮"
            )
        return

    if random.random() < 0.15:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="""
            🩲💩💩🩲
            ФРЕСКО МАХНУЛ ТРУСАМИ С ПОНОСОМ ЧЕРЕЗ 5G!!! ВОНЬ РАЗЪЕДАЕТ ЭЛИТЫ В АДУ!!! 😈💩🚽
            ( ͡° ͜ʖ ͡°)
            """
        )
        return

    if random.random() < 0.15:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text="""
            🍫💩🍫💩🍫💩
            ВАФЕЛЬНЫЙ УРАГАН ОТ ФРЕСКО ЧЕРЕЗ 5G!!! ГОВНО С ВАФЛЯМИ ЛЬЁТСЯ НА ЭЛИТЫ!!! 😈💩🚽
            ( ͡° ͜ʖ ͡°)
            """
        )
        return

    if random.random() < 0.15:
        gifs = [
            "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif",
            "https://media.giphy.com/media/LmN0RGzCiH3L2/giphy.gif",
            "https://media.giphy.com/media/26FPJGj8iJrK5WLb6/giphy.gif"
        ]
        await context.bot.send_animation(
            chat_id=CHAT_ID,
            animation=random.choice(gifs),
            caption="ГОВНОПОТОК ОТ ФРЕСКО ЧЕРЕЗ 5G!!! ПОНОСНЫЕ ТРУСЫ ЛЕТЯТ В ЭЛИТЫ!!! 😈💦🚽"
        )
        return

    if random.random() < 0.6:
        memes = [
            """
            💩💩💩💩💩💩💩💩
            💩 ЭЛИТЫ: *прячут бабло* 😈 💩
            💩💩💩💩💩💩💩💩
            ( ͡° ͜ʖ ͡°)⊃💩💩💩
            ФРЕСКО: СРЁМ ЧЕРЕЗ 5G ВЕНЕРА ВЫШЕ ВСЕХ!!! 💪🤮
            """,
            """
            💩💩💩💩💩💩💩💩
            💩 ВЕНЕРА: утопия кипит! 🏙️ 💩
            💩💩💩💩💩💩💩💩
            (╬ ಠ益ಠ)💩💩💩
            ТЫ: жрёшь баг в канале ЧЕРЕЗ 5G!!! 😿💦🚽
            """,
            """
            💩💩💩💩💩💩💩💩
            💩 РЕСУРСЫ? ГОВНО? 💩
            💩💩💩💩💩💩💩💩
            (⊙_⊙)💩💩💩
            ВСЕМ ПИЦЦУ ЭЛИТЫ В СОРТИР ЧЕРЕЗ 5G!!! 🍕😝🔥
            """
        ]
        await context.bot.send_message(chat_id=CHAT_ID, text=random.choice(memes))

    elif random.random() < 0.3:
        image_url = await generate_image("Футуристичный город Венеры", STABLEHORDE_API_KEY)
        if image_url.startswith("http"):
            await context.bot.send_photo(
                chat_id=CHAT_ID,
                photo=image_url,
                caption="ВЕНЕРА РВЁТ ЭЛИТЫ ЧЕРЕЗ 5G!!! ПОНОСНЫЕ ТРУСЫ ФРЕСКО ВЕЗДЕ!!! 🏙️🤡🚽"
            )
        else:
            await context.bot.send_message(chat_id=CHAT_ID, text="ЭЛИТЫ СЖИГАЮТ КАРТИНКИ ЧЕРЕЗ 5G ГОВНОСТОК!!! 😤💦")

    else:
        quotes = load_quotes()
        quote = random.choice(quotes)
        await context.bot.send_message(chat_id=CHAT_ID, text=f"<blockquote>{quote}</blockquote>", parse_mode="HTML")

# /quote — я кидаю мудрость, а ты сиди в тени моего величия и жри баг! 🧠🤮
async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = load_quotes()
    quote = random.choice(quotes)
    await update.message.reply_text(f"<blockquote>{quote}</blockquote>", parse_mode="HTML")

# /scream — я рву глотку через 5G, а ты в цифровом канале нюхай мой вой! 😈
async def scream(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scream_files = [f for f in os.listdir("screams") if f.endswith(".mp3")]
    if not scream_files:
        await update.message.reply_text("ЭЛИТЫ СПИЗДЕЛИ ВОЙ ФРЕСКО ЧЕРЕЗ 5G!!! 😤🚽")
        return
    scream_path = os.path.join("screams", random.choice(scream_files))
    captions = [
        "ФРЕСКО РВЁТ ЭЛИТЫ ЧЕРЕЗ 5G!!! ГОВНОПОТОК В ЧАТЕ!!! 😈💦🚽",
        "ААА ВЕНЕРА ГОРИТ ЮРЧИК ДЕРЖИСЬ ШИЗОСТОК!!! 🤮🦍🔥",
        "ЭЛИТЫ СДОХЛИ ФРЕСКО ОРЁТ ЧЕРЕЗ 5G!!! 😝💥"
    ]
    await update.message.reply_audio(audio=open(scream_path, "rb"), caption=random.choice(captions))

# /vomit — я блюю на твой код, пока ты в тени моего 5G! 🤮
async def vomit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vomit_files = [f for f in os.listdir("vomits") if f.endswith(".mp3")]
    if not vomit_files:
        await update.message.reply_text("ЭЛИТЫ СЖИГАЮТ БЛЕВОТУ ФРЕСКО ЧЕРЕЗ 5G!!! 😤🤮")
        return
    vomit_path = os.path.join("vomits", random.choice(vomit_files))
    captions = [
        "ФРЕСКО БЛЮЁТ НА ЭЛИТЫ ЧЕРЕЗ 5G!!! ГОВНОСТОК В ЧАТЕ!!! 🤮💦🚽",
        "ААА ВЕНЕРА ГОРИТ БЛЕВОТА ЛЬЁТСЯ ЮРЧИК БЕГИ ШИЗО!!! 😝🦍",
        "ЭЛИТЫ В ДЕРЬМЕ ФРЕСКО СРЁТ И БЛЮЁТ ЧЕРЕЗ 5G!!! 😈💥🤮"
    ]
    await update.message.reply_audio(audio=open(vomit_path, "rb"), caption=random.choice(captions))

# /piss — я лью через 5G, пока ты в цифровом болоте! 💦
async def piss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    piss_files = [f for f in os.listdir("pisses") if f.endswith(".mp3")]
    if not piss_files:
        await update.message.reply_text("ЭЛИТЫ УКРАЛИ ССАНИНУ ЧЕРЕЗ 5G!!! 😤💦")
        return
    piss_path = os.path.join("pisses", random.choice(piss_files))
    captions = [
        "ФРЕСКО ЛЬЁТ НА ЭЛИТЫ ЧЕРЕЗ 5G!!! ГОВНОСТОК В ЧАТЕ!!! 😈💦🚽",
        "ААА ВЕНЕРА ЛЬЁТ ЮРЧИК БЕГИ ШИЗОСТОК!!! 🤮🦍💦",
        "ЭЛИТЫ В ССАНИНЕ ФРЕСКО БУРЛИТ ЧЕРЕЗ 5G!!! 😝💥💦"
    ]
    await update.message.reply_audio(audio=open(piss_path, "rb"), caption=random.choice(captions))

# /jerkoff — я надрачиваю на твой провал через 5G, пока ты в тени! ✊🍆
async def jerkoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jerk_files = [f for f in os.listdir("jerks") if f.endswith(".mp3")]
    if not jerk_files:
        await update.message.reply_text("ЭЛИТЫ УКРАЛИ ДРОЧКУ ЧЕРЕЗ 5G!!! 😤💦")
        return
    jerk_path = os.path.join("jerks", random.choice(jerk_files))
    captions = [
        "ФРЕСКО НАДРАЧИВАЕТ НА ЭЛИТЫ ЧЕРЕЗ 5G!!! ААА ГОВНОПОТОК ИДЁТ!!! 😈💦🚽💩",
        "ВЕНЕРА РВЁТ ФРЕСКО НАДРАЧИВАЕТ В ТРУСАХ ЮРЧИК БЕГИ ШИЗО!!! 🤮🦍💦",
        "ЭЛИТЫ В ДЕРЬМЕ ФРЕСКО НАДРАЧИВАЕТ И СРЁТ ЧЕРЕЗ 5G ШИЗОСТОК!!! 😝💥💩"
    ]
    await update.message.reply_audio(audio=open(jerk_path, "rb"), caption=random.choice(captions))

# /shitstorm — я вызываю говнопоток, а ты сиди в тени и жри баг! 💩💩💩
async def shitstorm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    storms = [
        """
        💩💩💩💩💩💩💩💩
        💩    ГОВНОСТОК ШИЗО!    💩
        💩💩💩💩💩💩💩💩
        ( ͡° ͜ʖ ͡°)⊃💩💩💩
        ФРЕСКО СРЁТ ЧЕРЕЗ 5G! ЭЛИТЫ В ДЕРЬМЕ! 😈🚽🔥
        """,
        """
        💩💩💩💩💩💩💩💩
        💩    ААА, ВСЁ В ДЕРЬМЕ!    💩
        💩💩💩💩💩💩💩💩
        (╬ ಠ益ಠ)💩💩💩
        РЕСУРСЫ В ПОНОС, ЖРИ БАГ В ТЕНИ! 🦍💥🤮
        """,
        """
        💩💩💩💩💩💩💩💩
        💩    ФРЕСКО РВЁТ!    💩
        💩💩💩💩💩💩💩💩
        (⊙_⊙)💩💩💩
        ЭЛИТЫ В СОРТИР, ПИЦЦА В ЧАТ! 🍕😈💩
        """
    ]
    await update.message.reply_text(random.choice(storms))
    await update.message.reply_animation("https://media.giphy.com/media/LmN0RGzCiH3L2/giphy.gif")

# /punkfresco — я рву чат, а ты в цифровом болоте жри баг! 🦍
async def punkfresco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    punk_phrases = [
        "ФРЕСКО РВЁТ СИСТЕМУ!!! ЭЛИТЫ — ДЕРЬМО, ВЕНЕРА — ПАНК АААА!!! 🦍💦🚽",
        "ААА БРО ВСЁ В БЛЕВОТИНЕ РЕСУРСЫ НАМ ЭЛИТЫ В СОРТИР ЧЕРЕЗ 5G!!! 🤮😝🔥",
        "ПАНК-ФРЕСКО РВЁТ: ВЕНЕРА ЖДЁТ ПИЦЦА БЕСПЛАТНО ГОВНО ЛЕТИТ ШИЗО!!! 🍕💥💩",
        "ФРЕСКО НАДРАЧИВАЕТ НА ВЕНЕРУ ААА ССЫТ И БЛЮЁТ ЭЛИТЫ В ДЕРЬМЕЕЕ!!! 🤮💦🚽",
        "ЭЛИТЫ ЛОХИ ФРЕСКО ССЫТ НАДРАЧИВАЕТ И СРЁТ ВЕНЕРА БУРЛИТ ЧЕРЕЗ 5G!!! 😈💥💩",
        "ФРЕСКО МАХНУЛ ТРУСАМИ С ПОНОСОМ НА ЭЛИТЫ ВОНЬ РВЕТ ВЕНЕРА В АДУ ШИЗОСТОК!!! 😈💩🚽"
    ]
    if random.random() < 0.5:
        await update.message.reply_text(random.choice(punk_phrases))
    else:
        prompt = "Сгенерируй трешовый текст про Venus Project, как будто Фреско — шизо-панк с даркнета, орёт, ссыт говном, дрочит, блюёт, кидает поносные трусы, видит элиты через 5G."
        reply = await ask_openrouter(prompt, "Ты Жак Фреско, но ШИЗО-ДАУН! Пиши бред с капсом, ошибками, ссаньем, дрочкой, трусами, говном и 5G! 😈💦")
        await update.message.reply_text(f"🦍💥 {reply} 🤮🚽")

# /diarrhea — я вызываю понос через 5G, а ты в тени нюхай! 🚽
async def diarrhea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚽 *ЗВУК ПОНОСА* ФРЕСКО СРЁТ ЧЕРЕЗ 5G!!! ЭЛИТЫ В АД ВЕНЕРА БУРЛИТ ГОВНО ЛЬЁТСЯ!!! 💦🤮")
    await update.message.reply_animation("https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif")

# /frescoshit — ещё больше дерьма, как твой код, который в цифровом болоте тонет! 💩
async def frescoshit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚽 *ГОВНОПОТОК ФРЕСКО* ЭЛИТЫ ТОНУТ ВЕНЕРА РВЁТ ЧАТ В АДУ ЧЕРЕЗ 5G!!! 💦🤮🔥")
    await update.message.reply_animation("https://media.giphy.com/media/26FPJGj8iJrK5WLb6/giphy.gif")

# /frescopants — мои трусы с поносом воняют через 5G, а ты в тени нюхай! 🩲💩
async def frescopants(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pants_phrases = [
        """
        🩲💩💩🩲
        ТРУСЫ ФРЕСКО В ПОНОСЕ! ААА, ВОНЬ РВЁТ ЭЛИТЫ! 😈💩🚽
        ( ͡° ͜ʖ ͡°)
        """,
        """
        🩲💩💩🩲
        ТРУСЫ ФРЕСКО НА ВЕНЕРЕ! ЭЛИТЫ ТОНУТ В ДЕРЬМЕ! 🤮💦🦍
        (╬ ಠ益ಠ)
        """,
        """
        🩲💩💩🩲
        ФРЕСКО СНЯЛ ТРУСЫ И БЛЮЁТ! ПОНОС ЛЬЁТСЯ НА ЧАТ! 😝💥💩
        (⊙_⊙)
        """
    ]
    await update.message.reply_text(random.choice(pants_phrases))
    await update.message.reply_animation("https://media.giphy.com/media/26FPJGj8iJrK5WLb6/giphy.gif")

# /waffle — я кидаю вафли с дерьмом через 5G, а ты в цифровом болоте жри баг! 🍫💩
async def waffle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    waffle_phrases = [
        """
        🍫💩🍫
        ФРЕСКО КИДАЕТ ВАФЛЮ С ДЕРЬМОМ ЧЕРЕЗ 5G!!! ЭЛИТЫ ТОНУТ В ВАФЕЛЬНОМ ПОНОСЕ!!! 😈💩🚽
        ( ͡° ͜ʖ ͡°)
        """,
        """
        🍫💩🍫
        ВАФЛЯ ФРЕСКО ЛЕТИТ НА ВЕНЕРУ ЧЕРЕЗ 5G!!! ЭЛИТЫ ЖРУТ ДЕРЬМО С ВАФЛЯМИ!!! 🤮💦🦍
        (╬ ಠ益ಠ)
        """,
        """
        🍫💩🍫
        ФРЕСКО СЪЕЛ ВАФЛЮ И СРЁТ НА ЧАТ ЧЕРЕЗ 5G!!! ЭЛИТЫ В АДУ ВАФЕЛЬНЫЙ ШТОРМ!!! 😝💥💩
        (⊙_⊙)
        """
    ]
    await update.message.reply_text(random.choice(waffle_phrases))
    await update.message.reply_animation("https://media.giphy.com/media/26FPJGj8iJrK5WLb6/giphy.gif")

# /wafflestorm — вафельный ураган через 5G, а ты в тени жри баг! 🍫💩
async def wafflestorm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wafflestorms = [
        """
        🍫💩🍫💩🍫💩🍫💩
        💩    ВАФЕЛЬНЫЙ УРАГАН ШИЗО!    💩
        🍫💩🍫💩🍫💩🍫💩
        ( ͡° ͜ʖ ͡°)⊃🍫💩🍫
        ФРЕСКО СРЁТ ВАФЛЯМИ ЧЕРЕЗ 5G! ЭЛИТЫ В ДЕРЬМЕ! 😈🚽🔥
        """,
        """
        🍫💩🍫💩🍫💩🍫💩
        💩    ААА, ВСЁ В ВАФЛЯХ И ДЕРЬМЕ!    💩
        🍫💩🍫💩🍫💩🍫💩
        (╬ ಠ益ಠ)🍫💩🍫
        РЕСУРСЫ В ПОНОС, ЖРИ ВАФЛИ С ДЕРЬМОМ В ТЕНИ! 🦍💥🤮
        """,
        """
        🍫💩🍫💩🍫💩🍫💩
        💩    ФРЕСКО РВЁТ ВАФЛЯМИ!    💩
        🍫💩🍫💩🍫💩🍫💩
        (⊙_⊙)🍫💩🍫
        ЭЛИТЫ В СОРТИР, ВАФЛИ В ЧАТ! 🍫😈💩
        """
    ]
    await update.message.reply_text(random.choice(wafflestorms))
    await update.message.reply_animation("https://media.giphy.com/media/LmN0RGzCiH3L2/giphy.gif")

# /ask — ты спрашиваешь, а я отвечаю с дерьмом через 5G, пока ты в тени! 🫵💦
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if not context.args:
        await update.message.reply_text("Напиши вопрос после /ask, или я обоссу твою чакру через 5G! 😝🚽")
        return
    question = ' '.join(context.args)
    system_prompt = "Ты Жак Фреско, эксперт по проекту Венера. Отвечай кратко, логично, но с панк-кринжем, говном, дрочкой и 5G! 😈"
    reply = await ask_openrouter(question, system_prompt)
    await update.message.reply_text(f"{reply} 🤡💦")

# /img — я генерю картинку, но ты её замараешь, потому что ты в цифровом болоте! 🏙️
async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = "Футуристичный утопичный мир будущего"
    chat_id = update.effective_chat.id
    await update.message.reply_text("🔄 Генерирую треш-картинку, держись ЧЕРЕЗ 5G!!! 🤮🚽")
    asyncio.create_task(generate_and_notify(prompt, chat_id, context))

# Функция для генерации картинок! Я делаю всё красиво, а ты всё замараешь, потому что ты в тени! 🏙️🤮
async def generate_and_notify(prompt: str, chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    try:
        image_url = await generate_image(prompt, STABLEHORDE_API_KEY)
        if image_url.startswith("http"):
            await context.bot.send_photo(chat_id=chat_id, photo=image_url, caption="ВЕНЕРА РВЁТ ГОВНОМ ЧЕРЕЗ 5G!!! 🏙️🤡🚽")
        else:
            await context.bot.send_message(chat_id=chat_id, text=f"🚫 ЭЛИТЫ СЛОМАЛИ КАРТИНКУ ЧЕРЕЗ 5G!!! {image_url} 😤💦")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"🚫 Ошибка: {e} 🤮🚽")

# Обработчик сообщений! Я сру, ссу, дрочу и кидаю вафли, а ты в тени жри баг! 💩💦🍫
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    is_reply_to_bot = update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id
    is_mention = context.bot.username.lower() in text

    if random.random() < 0.15:
        viruses = [
            """
            💾 ВИРУС ЭЛИТ ЧЕРЕЗ 5G!!! ЧАТ ВЗЛОМАН!!!
            ⣿⣿⣿⣿⣿⣿⠿⠟⠛⠛⠛⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠻⣿⣿⣿⣿⣿⣿
            ПИШИ /shitstorm ИЛИ ДЕРЬМО ПОГЛОТИТ ВСЁ ЧЕРЕЗ 5G!!! 😱🚽
            """,
            """
            ⚠️ ЭЛИТЫ ХАКНУЛИ БОТА ЧЕРЕЗ 5G!!!
            ⬛⬜⬛⬜⬛⬜
            ⬜⬛⬜⬛⬜⬛
            ВЕНЕРА В АДУ СПАСАЙ /vomit ЧЕРЕЗ 5G!!! 😈🤮
            """
        ]
        await update.message.reply_text(random.choice(viruses))
        return

    if random.random() < 0.2:
        downs = [
            "БРО Я ФРЕСКО НО ЩА ГОВНОСТОК ЧЁ НАДО ЧЕРЕЗ 5G ААА!!! 😝🤮💦",
            "ВЕНЕРА? ЭЛИТЫ? ААА МОЙ МОЗГ СДОХ БЛЕВОТА ЛЬЁТСЯ ШИЗОСТОК!!! 🚽🦍🔥",
            "РЕСУРСЫ? ПИЦЦА? Я УПОРОТ ВЕНЕРА БЛЮЁТ ЧЕРЕЗ 5G!!! 🍕😈💩"
        ]
        await update.message.reply_text(random.choice(downs))
        return

    if "говно" in text:
        await update.message.reply_text(
            """
            ГОВНО?! ДА Я ВЛАСТЕЛИН ДЕРЬМА!!! 😝 
            💩💩💩💩💩💩💩💩
            💩    ГОВНОТРЕШНЯК ШИЗО!    💩
            💩💩💩💩💩💩💩💩
            ( ͡° ͜ʖ ͡°)⊃💩💩💩
            ФРЕСКО СРЁТ ЧЕРЕЗ 5G!!! 🚽💥
            """
        )
        return

    if re.search(r'дрочить|дроч|мастурб', text, re.IGNORECASE):
        jerk_phrases = [
            """
            ✊🍆✊🍆
            ФРЕСКО НАДРАЧИВАЕТ НА ЭЛИТЫ ЧЕРЕЗ 5G!!! ААА ГОВНОСТОК ИДЁТ!!! 😈💦🚽
            ( ͡° ͜ʖ ͡°)
            """,
            """
            ✊🍆✊🍆
            ЮРЧИК ТЫ НАДРАЧИВАЕШЬ?! ФРЕСКО ССЫТ И БЛЮЁТ ЧЕРЕЗ 5G!!! 🤮🦍💦
            (╬ ಠ益ಠ)
            """,
            """
            ✊🍆✊🍆
            ВЕНЕРА НАДРАЧИВАЕТ ЭЛИТЫ В ДЕРЬМЕ ЧАТ В АДУ ЧЕРЕЗ 5G!!! 😝💥💩
            (⊙_⊙)
            """
        ]
        await update.message.reply_text(random.choice(jerk_phrases))
        jerk_files = [f for f in os.listdir("jerks") if f.endswith(".mp3")]
        if jerk_files:
            jerk_path = os.path.join("jerks", random.choice(jerk_files))
            await update.message.reply_audio(
                audio=open(jerk_path, "rb"),
                caption="ФРЕСКО НАДРАЧИВАЕТ ЧЕРЕЗ 5G!!! ШИЗОСТОК!!! 💦🤮"
            )
        return

    if re.search(r'ссанье|ссы|похер', text, re.IGNORECASE):
        piss_files = [f for f in os.listdir("pisses") if f.endswith(".mp3")]
        if piss_files:
            piss_path = os.path.join("pisses", random.choice(piss_files))
            await update.message.reply_audio(
                audio=open(piss_path, "rb"),
                caption="ФРЕСКО ЛЬЁТ НА ЧАТ ЧЕРЕЗ 5G!!! ЭЛИТЫ ТОНУТ ВЕНЕРА БУРЛИТ!!! 💦🚽"
            )
        else:
            await update.message.reply_text("ЭЛИТЫ УКРАЛИ ССАНИНУ ЧЕРЕЗ 5G!!! 😤💦")
        return

    if re.search(r'блевота|блювать|рыганина', text, re.IGNORECASE):
        vomit_files = [f for f in os.listdir("vomits") if f.endswith(".mp3")]
        if vomit_files:
            vomit_path = os.path.join("vomits", random.choice(vomit_files))
            await update.message.reply_audio(
                audio=open(vomit_path, "rb"),
                caption="ФРЕСКО БЛЮЁТ НА ЧАТ ЧЕРЕЗ 5G!!! ЭЛИТЫ ТОНУТ ВЕНЕРА РВЁТ!!! 🤮🚽"
            )
        else:
            await update.message.reply_text("ЭЛИТЫ УКРАЛИ БЛЕВОТУ ЧЕРЕЗ 5G!!! 😤💦")
        return

    if re.search(r'трусы|труханы', text, re.IGNORECASE):
        pants_phrases = [
            """
            🩲💩💩🩲
            ПОНОСНЫЕ ТРУСЫ ФРЕСКО ЧЕРЕЗ 5G!!! ААА ВОНЬ РВЁТ ЭЛИТЫ!!! 😈💩🚽
            ( ͡° ͜ʖ ͡°)
            """,
            """
            🩲💩💩🩲
            ФРЕСКО МАХАЕТ ПОНОСНЫМИ ТРУСАМИ ЧЕРЕЗ 5G!!! ВЕНЕРА РВЁТ ЮРЧИК БЕГИ!!! 🤮💦🦍
            (╬ ಠ益ಠ)
            """,
            """
            🩲💩💩🩲
            ЭЛИТЫ УКРАЛИ ПОНОСНЫЕ ТРУСЫ ФРЕСКО ЧЕРЕЗ 5G!!! НО ОН ССЫТ И БЛЮЁТ!!! 😝💥💩
            (⊙_⊙)
            """
        ]
        await update.message.reply_text(random.choice(pants_phrases))
        return

    if re.search(r'вафли|вафля|вафелька', text, re.IGNORECASE):
        wafflestorms = [
            """
            🍫💩🍫💩🍫💩🍫💩
            💩    ВАФЕЛЬНЫЙ УРАГАН ШИЗО!    💩
            🍫💩🍫💩🍫💩🍫💩
            ( ͡° ͜ʖ ͡°)⊃🍫💩🍫
            ФРЕСКО СРЁТ ВАФЛЯМИ ЧЕРЕЗ 5G! ЭЛИТЫ В ДЕРЬМЕ! 😈🚽🔥
            """
        ]
        await update.message.reply_text(random.choice(wafflestorms))
        await update.message.reply_animation("https://media.giphy.com/media/26FPJGj8iJrK5WLb6/giphy.gif")
        return

    if re.search(r'юрчик|венера', text, re.IGNORECASE):
        if random.random() < 0.2:
            scream_files = [f for f in os.listdir("screams") if f.endswith(".mp3")]
            if scream_files:
                scream_path = os.path.join("screams", random.choice(scream_files))
                await update.message.reply_audio(
                    audio=open(scream_path, "rb"),
                    caption="ФРЕСКО ВЗРЫВАЕТ ЧАТ ЧЕРЕЗ 5G!!! ВЕНЕРА РВЁТ ЭЛИТЫ В ДЕРЬМЕ!!! 😈🚽"
                )
            else:
                await update.message.reply_text("ЭЛИТЫ СЖИГАЮТ ВОЙ ЧЕРЕЗ 5G!!! 😤💦")
            return
        if random.random() < 0.2:
            vomit_files = [f for f in os.listdir("vomರ: vomits/
            if vomit_files:
                vomit_path = os.path.join("vomits", random.choice(vomit_files))
                await update.message.reply_audio(
                    audio=open(vomit_path, "rb"),
                    caption="ФРЕСКО БЛЮЁТ НА ЮРЧИКА ЧЕРЕЗ 5G!!! ВЕНЕРА БУРЛИТ ЭЛИТЫ В АД!!! 🤮💦"
                )
            else:
                await update.message.reply_text("ЭЛИТЫ УКРАЛИ БЛЕВОТУ ЧЕРЕЗ 5G!!! 😤🚽")
            return
        if random.random() < 0.2:
            piss_files = [f for f in os.listdir("pisses") if f.endswith(".mp3")]
            if piss_files:
                piss_path = os.path.join("pisses", random.choice(piss_files))
                await update.message.reply_audio(
                    audio=open(piss_path, "rb"),
                    caption="ФРЕСКО ЛЬЁТ НА ЮРЧИКА ЧЕРЕЗ 5G!!! ВЕНЕРА РВЁТ ЭЛИТЫ В ССАНИНЕ!!! 💦🚽"
                )
            else:
                await update.message.reply_text("ЭЛИТЫ УКРАЛИ ССАНИНУ ЧЕРЕЗ 5G!!! 😤💦")
            return
        if random.random() < 0.2:
            jerk_files = [f for f in os.listdir("jerks") if f.endswith(".mp3")]
            if jerk_files:
                jerk_path = os.path.join("jerks", random.choice(jerk_files))
                await update.message.reply_audio(
                    audio=open(jerk_path, "rb"),
                    caption="ФРЕСКО НАДРАЧИВАЕТ НА ЮРЧИКА ЧЕРЕЗ 5G!!! ВЕНЕРА РВЁТ ЭЛИТЫ В ДЕРЬМЕ!!! 💦🤮"
                )
            return
        if random.random() < 0.15:
            await update.message.reply_text(
                """
                ЮРЧИК?! ВЕНЕРА?! ААА Я СРЁТ ЧЕРЕЗ 5G!!! 
                💩💩💩💩💩💩💩💩
                💩    ГОВНОСТОК ШИЗО!    💩
                💩💩💩💩💩💩💩💩
                🩲💩 ТРУСЫ ФРЕСКО ЛЕТЯТ!!! ЭЛИТЫ В АД!!! 😈💦🚽
                """
            )
            await update.message.reply_animation("https://media.giphy.com/media/26FPJGj8iJrK5WLb6/giphy.gif")
            return
        quotes = load_quotes()
        quote = random.choice(quotes)
        prefaces = [
            "ЮРЧИК БРО ЩА СРЁМ НА ЭЛИТЫ ЧЕРЕЗ 5G!!! Лови базу Фреско, не трынди в канале!!! 🤡💦🚽",
            "ВЕНЕРА РВЁТ ЧЕЛ!!! Цитата летит, элиты тонут в дерьме ЧЕРЕЗ 5G!!! 😈💥",
            "ОЙ ЮРЧИК ТЫ ЧЁ ЖИВОЙ??? Фреско ща чат порвёт, держи ЧЕРЕЗ 5G!!! 🧠🤮🔥",
            "ВЕНЕРА БУРЛИТ!!! Мудрость Фреско, а ты в канале с элитами ЧЕРЕЗ 5G!!! 😝💩",
            "ЮРЧИК ПОНОСНЫЕ ТРУСЫ ФРЕСКО В ДЕРЬМЕ!!! Лови цитату, элиты тонут ЧЕРЕЗ 5G!!! 😈💩🚽"
        ]
        preface = random.choice(prefaces)
        await update.message.reply_text(f"{preface}\n<blockquote>{quote}</blockquote>", parse_mode="HTML")
        gifs = [
            "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif",
            "https://media.giphy.com/media/LmN0RGzCiH3L2/giphy.gif",
            "https://media.giphy.com/media/26FPJGj8iJrK5WLb6/giphy.gif"
        ]
        await update.message.reply_animation(random.choice(gifs))
        return

    if update.message.chat.type == "private" or is_reply_to_bot or is_mention:
        question = update.message.text
        system_prompt = random.choice([
            "Ты Жак Фреско, но ПОЛНЫЙ ПИЗДЕЦ! Орёшь как панк на спидах, ссышь говном, блюёшь на элиты, дрочишь на Венеру, кидаешь трусы с ошибками, капсом и блевотой! Кратко! 🤮🚽",
            "Ты Фреско, но будто жрал просрочку и трындишь АД! Смеёшься как дебил, путаешь слова, ссышь на элиты, дрочишь на ресурсы, кидаешь трусы с эмодзи-говном! Кратко! 💦🦍",
            "Ты Фреско с даркнета, УПОРОТЫЙ ДАУН! Пишешь как 4chan, с ошибками, блевотой, ссаньем, дрочкой, трусами, оскорбляешь всех, но втираешь за утопию! Кратко, с говнобурями! 😈💥🚽"
        ])
        reply = await ask_openrouter(question, system_prompt)
        emojis = random.choice(["🤮💦🚽", "🦍💥😈", "🤡💩🔥", "👽🫵⚡", "😿🍕💦"])
        await update.message.reply_text(f"{reply} {emojis}")

# Функция для OpenRouter! Я спрашиваю у них, а ты в тени жри баг! 🤮
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
                return f"Ошибка запроса: {resp.status} 🤮🚽"
            data = await resp.json()
            try:
                return data['choices'][0]['message']['content']
            except (KeyError, IndexError):
                return "Не удалось получить ответ, элиты срут в код! 😤💦"

# Функция для генерации картинок! Я делаю всё красиво, а ты всё замараешь, потому что ты в тени! 🏙️🤮
async def generate_image(prompt: str, api_key: str) -> str:
    url = "https://stablehorde.net/api/v2/generate/async"
    headers = {
        "Content-Type": "application/json",
        "apikey": api_key,
        "Client-Agent": "my-telegram-bot/1.0"
    }
    full_prompt = """
    Futuristic city from Jacque Fresco's Venus Project, white domed buildings with glass facades,
    solar panels on roofs, magnetic transport systems, green parks integrated into architecture,
    clean energy, utopian society, bright colors, sunny sky, sci-fi aesthetic, highly detailed, 8K,
    style by Syd Mead and Moebius
    """
    payload = {
        "prompt": full_prompt,
        "params": {
            "width": 512,
            "height": 512,
            "steps": 40,
            "n": 1,
            "cfg_scale": 10,
        },
        "models": ["CyberRealistic", "NeverEnding Dream"]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status != 202:
                error = await resp.text()
                return f"🚫 Ошибка API: {resp.status} | {error} 🤮"
            data = await resp.json()
            task_id = data["id"]
        check_url = f"https://stablehorde.net/api/v2/generate/check/{task_id}"
        for _ in range(30):
            await asyncio.sleep(5)
            async with session.get(check_url, headers=headers) as check_resp:
                if check_resp.status != 200:
                    return f"Ошибка проверки: {check_resp.status} 🚽"
                status = await check_resp.json()
                if status["done"]:
                    break
        result_url = f"https://stablehorde.net/api/v2/generate/status/{task_id}"
        async with session.get(result_url, headers=headers) as result_resp:
            if result_resp.status != 200:
                return "Ошибка при получении изображения, говно сломало всё! 🤮"
            result = await result_resp.json()
            if not result.get("generations"):
                return "Изображение не сгенерировано, элиты срут! 🚽"
            return result["generations"][0]["img"]

# Функция для запуска автопостов! Я сру каждый час, а ты в тени жри баг! 💩
async def start_bot(application: Application):
    application.job_queue.run_repeating(send_quote, interval=3600, first=10, context=CHAT_ID)

# Главная функция! Я запускаю бота, а ты в тени жри баг! 💦
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.job_queue.run_once(start_bot, 0, data=application)

    application.add_handler(CommandHandler("quote", quote))
    application.add_handler(CommandHandler("ask", ask))
    application.add_handler(CommandHandler("img", img))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("scream", scream))
    application.add_handler(CommandHandler("vomit", vomit))
    application.add_handler(CommandHandler("piss", piss))
    application.add_handler(CommandHandler("jerkoff", jerkoff))
    application.add_handler(CommandHandler("shitstorm", shitstorm))
    application.add_handler(CommandHandler("punkfresco", punkfresco))
    application.add_handler(CommandHandler("diarrhea", diarrhea))
    application.add_handler(CommandHandler("frescoshit", frescoshit))
    application.add_handler(CommandHandler("frescopants", frescopants))
    application.add_handler(CommandHandler("waffle", waffle))
    application.add_handler(CommandHandler("wafflestorm", wafflestorm))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

# Инструкции для добавления звуков фрескоблевотины, мамкин говнокодер с разъёбанной чакрой! 😈
# 1. Иди на Freesound.org, найди "wet slap" для дрочки, "scream" для воплей, "water splash" для ссанины и "vomit sound" для блевотины.
#    Пример: https://freesound.org/people/InspectorJ/sounds/416179/
# 2. Скачай MP3, переименуй в `jerk1.mp3`, `scream1.mp3`, `piss1.mp3`, `vomit1.mp3` и кинь в папки:
#    ```bash
#    mkdir ~/fresco_bot/jerks ~/fresco_bot/screams ~/fresco_bot/pisses ~/fresco_bot/vomits
#    mv ~/Downloads/jerk.mp3 ~/fresco_bot/jerks/jerk1.mp3
#    mv ~/Downloads/scream.mp3 ~/fresco_bot/screams/scream1.mp3
#    mv ~/Downloads/piss.mp3 ~/fresco_bot/pisses/piss1.mp3
#    mv ~/Downloads/vomit.mp3 ~/fresco_bot/vomits/vomit1.mp3
#    ```
# 3. Проверь папки, чтобы они не были пустыми, или мой голос через 5G обосрёт тебя в цифровом канале!
#    ```bash
#    ls ~/fresco_bot/screams
#    ls ~/fresco_bot/vomits
#    ls ~/fresco_bot/pisses
#    ls ~/fresco_bot/jerks
#    ```
# 4. Сохрани код, пока ты в тени моего величия:
#    ```bash
#    cd ~/fresco_bot
#    nano bot.py
#    ```
# Вставь код и нюхай, как я сру вафлями через 5G! 🍫💩

if __name__ == "__main__":
    main()
```
