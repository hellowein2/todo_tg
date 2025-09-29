FROM my_base:latest

WORKDIR /app

COPY ./app /app/

EXPOSE 80

CMD ["uvicorn", "main_web:app", "--host", "0.0.0.0", "--port", "80"]