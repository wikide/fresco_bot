# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы бота
COPY . .

# 1. Устанавливаем FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir \
    python-telegram-bot==20.3 \
    aiohttp==3.9.5 \
    python-dotenv \
    SpeechRecognition==3.10.0 \
    pydub==0.25.1 \
    ffmpeg-python==0.2.0 \
    openai==1.12.0 \
    numpy==1.26.4

# Запускаем бота
CMD ["python", "run.py"]
