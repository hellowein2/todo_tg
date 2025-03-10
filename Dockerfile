# Используем Python как базовый образ
FROM python:3.12.3

# Установим необходимые пакеты для управления локалями
RUN apt-get update && apt-get install -y locales

# Активируем русскую локаль
RUN sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8

# Установим рабочую директорию
WORKDIR /app

# Скопировать файл зависимостей в контейнер
COPY requirements.txt .

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопировать все необходимые файлы в контейнер
COPY . .

# Команда запуска приложения
CMD ["python", "main.py"]