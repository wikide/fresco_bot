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

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir python-telegram-bot==20.3 aiohttp==3.9.5 python-dotenv

# Запускаем бота
CMD ["python", "run.py"]
