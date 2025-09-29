FROM my_base:latest

WORKDIR /app

COPY ./web_app /app/

EXPOSE 80

CMD ["uvicorn", "main_web:web_app", "--host", "0.0.0.0", "--port", "80"]