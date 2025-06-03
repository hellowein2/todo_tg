from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import Database
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import hmac
from urllib.parse import parse_qsl
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


def check_init_data(init_data: str, bot_token: str):
    data = dict(parse_qsl(init_data))

    if 'hash' not in data:
        raise ValueError("No hash in init_data")

    data.pop('signature', None)

    hash_to_check = data.pop('hash')
    hash_to_check = unquote(hash_to_check)

    data_check_arr = [f"{k}={v}" for k, v in sorted(data.items())]
    data_check_string = "\n".join(data_check_arr)

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    print("Calculated hash:", calculated_hash)
    print("Hash to check:", hash_to_check)

    is_valid = calculated_hash == hash_to_check
    return is_valid, data



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
async def verify(request: Request):
    body = await request.json()
    init_data = body.get('initData')
    print("Получен initData:", init_data)
    print("API_TOKEN:", API_TOKEN)

    if not init_data:
        raise HTTPException(status_code=400, detail="initData missing")

    if isinstance(init_data, dict):
        # Конвертируем словарь назад в строку параметров
        init_data_str = urlencode(init_data, doseq=True)
    elif isinstance(init_data, str):
        init_data_str = init_data
    else:
        raise HTTPException(status_code=422, detail="initData has unexpected type")

    if not API_TOKEN or API_TOKEN.strip() == "":
        print("Ошибка: BOT_TOKEN не установлен!")
        raise HTTPException(status_code=422, detail="Server configuration error: BOT_TOKEN missing")

    try:
        valid, user_data = check_init_data(init_data_str, API_TOKEN)
    except Exception as e:
        print("Ошибка в check_init_data:", e)
        raise HTTPException(status_code=422, detail=f"Check init_data error: {str(e)}")

    if not valid:
        print("Ошибка: Некорректная подпись initData", user_data)
        raise HTTPException(status_code=422, detail="Invalid initData hash")

    print("initData проверен успешно, user_data:", user_data)
