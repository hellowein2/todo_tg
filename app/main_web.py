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
    # Парсим строку параметров в список кортежей [(key, value), ...]
    params_list = parse_qsl(init_data, keep_blank_values=True)

    # Превращаем в словарь
    params = dict(params_list)

    # Убираем поля, которые не должны участвовать в подписи
    params.pop('hash', None)
    params.pop('signature', None)

    # Сортируем по ключам
    sorted_items = sorted(params.items())

    # Формируем строку для проверки
    data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted_items)

    return data_check_string


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





@app.post("/verify")
async def verify(data: InitDataRequest):
    init_data = data.initData
    print("Получен initData:", init_data)
    data_check_string = make_data_check_string(init_data)

    secret_key = hashlib.sha256(API_TOKEN.encode()).digest()

    params = parse_qs(init_data)

    # Получаем hash (он будет в списке, берем первый элемент)
    hash_value = params.get('hash', [None])[0]

    print("Hash:", hash_value)


    if hmac.new(secret_key, data_check_string.encode('utf-8'),
                hashlib.sha256).hexdigest() == hash_value:
        print('УРААААААА')


    return {"message": "Данные получены", "received_initData": init_data}

