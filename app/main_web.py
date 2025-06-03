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





@app.post("/verify")
async def verify(data: InitDataRequest):
    init_data = data.initData
    print("Получен initData:", init_data)

    data_check_string = make_data_check_string(init_data)
    secret_key = hashlib.sha256(API_TOKEN.encode()).digest()
    params = dict(parse_qsl(init_data))
    hash_value = params.get('hash', None)

    print("Hash из данных:", hash_value)
    print("Data-check-string:\n", data_check_string)
    return {'data': data_check_string}

    # if hash_value is None:
    #     return {"error": "Hash отсутствует в данных"}
    #
    # calculated_hash = hmac.new(secret_key, data_check_string.encode('utf-8'), hashlib.sha256).hexdigest()
    #
    # if calculated_hash == hash_value:
    #     print('УРААААААА - подпись верна!')
    #     return {"status": "valid"}
    # else:
    #     print('Подпись не совпадает!')
    #     return {"status": "invalid"}

