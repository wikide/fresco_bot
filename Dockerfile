# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы бота
COPY . .

# 1. Устанавливаем FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Установка самой свежей версии yt-dlp
RUN pip install --no-cache-dir git+https://github.com/yt-dlp/yt-dlp.git@master

# Устанавливаем зависимости Python

RUN pip install --no-cache-dir -r requirements.txt

# Запускаем бота
CMD ["python", "run.py"]
