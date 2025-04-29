# Telegram Bot Жак Фреско

Шуточный телеграмм бот с поддержкой голосовых команд

## 🚀 Возможности бота

- Генерация изображений по запросу
- Ответы на вопросы (текстовые и голосовые)
- Случайные цитаты
- Поддержка голосовых команд
- И многое другое

## 🛠 Установка и запуск

### Предварительные требования
- Docker установленный на системе
- Переменные окружения (токены API и т.д.)

### 🔧 Использование Makefile

```bash
# Собрать Docker-образ
make build

# Запустить контейнер
make run TOKEN=your_telegram_token CHAT_ID=your_chat_id

# Остановить контейнер
make stop

# Просмотр логов
make logs

# Полная пересборка и запуск
make deploy TOKEN=your_telegram_token CHAT_ID=your_chat_id

# Перезапуск контейнера
make restart

```
### Переменные окружения

Необходимо установить следующие переменные:

- TOKEN - Токен Telegram бота

- OPENROUTER_API_KEY - Ключ API OpenRouter

- STABLEHORDE_API_KEY - Ключ API StableHorde

- HF_API_KEY - Ключ API HuggingFace

## ⚙️ Настройка окружения

### Конфигурация через .env файл

Перед запуском создайте файл `.env` в корне проекта и укажите в нем необходимые переменные:

```bash
TELEGRAM_TOKEN=ваш_токен_бота
OPENROUTER_API_KEY=ваш_ключ_openrouter
STABLEHORDE_API_KEY=ваш_ключ_stablehorde 
HF_API_KEY=ваш_ключ_huggingface
```

## 🐳 Docker-развертывание

1. Создайте .env файл (см. выше)
2. Соберите образ
```
make build ; make run 
```
одной командой:
```
make deploy
```

### 🌐 Контакты и поддержка
Связаться с командой разработчиков: [Telegram Chat](https://t.me/+Et1vrcDMRmkxNzcy)

Поддержать проект: USDT (TRC20) ```TREqCkanrRjkRQ3PUHsowCtHAqFJ9kaaL1```

## 📜 Лицензия

Проект распространяется под [MIT License](https://opensource.org/licenses/MIT).

Полный текст лицензии:
```text
MIT License

Copyright (c) [2025] [OLYMP]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.