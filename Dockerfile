# Используем Python как базовый образ
FROM python:3.13.1

# Установим рабочую директорию
WORKDIR /usr/src/app

# Скопировать все файлы в контейнер
COPY . .

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Команда запуска приложения
CMD ["python", "./main.py"]
