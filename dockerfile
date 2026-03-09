# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы бота в контейнер
COPY . .


# Запускаем бота
ENTRYPOINT ["python", "bot.py"]