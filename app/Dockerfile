# Используем официальный Python образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы приложения
COPY . .

# Указываем порт, который будет прослушивать наш сервер внутри контейнера
EXPOSE 80

# Команда для запуска приложения
CMD ["uvicorn", "main-web:app", "--host", "0.0.0.0", "--port", "80"]