import urllib
from time import time

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import Database
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import hmac
from urllib.parse import parse_qsl, parse_qs
import os
from urllib.parse import urlencode, unquote

db = Database('ignore/data.db')
API_TOKEN = os.environ.get('BOT_TOKEN')

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешение запросов с любых источников
    allow_credentials=True,
    allow_methods=["*"],  # Разрешение всех методов, таких как GET и POST
    allow_headers=["*"],  # Разрешение всех заголовков
)


class Task(BaseModel):
    task: str

class InitDataRequest(BaseModel):
    initData: str



def make_data_check_string(init_data: str) -> str:
    params_list = parse_qsl(init_data, keep_blank_values=True)
    # Не превращай в dict, а оставь список, чтобы сохранить порядок и точные значения
    filtered = [(k, v) for k, v in params_list if k not in ('hash', 'signature')]
    filtered.sort(key=lambda x: x[0])
    return '\n'.join(f"{k}={v}" for k, v in filtered)


@app.post("/tasks")
async def add_task(task: Task):
    db.create_task(user_id=1014139378, task=task.task)
    return {"message": "Задача добавлена", "task": task.task}


@app.delete("/tasks/{task_name}")
async def delete_task(task_name: str):
    db.delete_task_with_name(user_id=1014139378, task=task_name)
    return {"message": "Задача удаленна", "task": task_name}


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    print(API_TOKEN)
    p, c = db.get_tasks(1014139378)
    pending_tasks = [f"{i[1]}" for i in p]
    completed_tasks = [f"{i[1]}" for i in c]
    return templates.TemplateResponse('index.html', {'request': request,
                                                     'pending_tasks': pending_tasks,
                                                     'completed_tasks': completed_tasks})


async def validate_telegram_init_data(init_data: str) -> bool:
    # Парсим initData
    parsed_data = urllib.parse.parse_qs(init_data)
    if not parsed_data.get("hash") or not parsed_data.get("auth_date"):
        return False

    # Извлекаем hash и auth_date
    received_hash = parsed_data["hash"][0]
    auth_date = int(parsed_data["auth_date"][0])

    # Проверяем, что auth_date не слишком старая (например, не старше 24 часов)
    if abs(time() - auth_date) > 86400:
        return False

    # Создаем секретный ключ
    secret_key = hmac.new(b"WebAppData", API_TOKEN.encode(), hashlib.sha256).digest()

    # Формируем строку данных для проверки
    data_check_string = []
    for key, value in parsed_data.items():
        if key != "hash":
            data_check_string.append(f"{key}={value[0]}")

    data_check_string = "\n".join(sorted(data_check_string))

    # Вычисляем HMAC-SHA-256
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    # Сравниваем с полученным hash
    return computed_hash == received_hash
@app.post("/verify")
async def verify(request: InitDataRequest):
    is_valid = await validate_telegram_init_data(request.initData)
    if not is_valid:
        raise HTTPException(status_code=403, detail="Некорректная initData")
    return {"status": "valid"}

