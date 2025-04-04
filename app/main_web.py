from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import Database

db = Database('ignore/data.db')

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    p, c = db.get_tasks(1014139378)
    pending_tasks = [f"{i[1]}" for i in p]
    completed_tasks = [f"{i[1]}" for i in c]
    return templates.TemplateResponse('index.html', {'request': request,
                                                     'pending_tasks': pending_tasks,
                                                     'completed_tasks': completed_tasks})
