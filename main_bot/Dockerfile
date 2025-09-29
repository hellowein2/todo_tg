FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY main_bot.py /app/main_bot.py

CMD ["python", "/app/main_bot.py"]