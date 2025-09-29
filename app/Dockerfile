FROM base:lastest

WORKDIR /app

COPY app/ /app/

EXPOSE 80

CMD ["uvicorn", "app.main_web:app", "--host", "0.0.0.0", "--port", "80"]