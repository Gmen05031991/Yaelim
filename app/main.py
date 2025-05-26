from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import engine, Base
from app.routers import companies, employees, tasks, notes
from app.models import employee, company, document, task, note
from datetime import datetime, timedelta
import os

# Создание папок
os.makedirs("app/data", exist_ok=True)
os.makedirs("app/uploads", exist_ok=True)
os.makedirs("app/static/img", exist_ok=True)
os.makedirs("app/templates", exist_ok=True)

# Инициализация приложения
app = FastAPI(
    title="Yaelim HR Cloud",
    description="ניהול עובדים עם מסמכים, ויזות ומשימות",
    version="1.0.0",
    debug=True
)

# Подключение шаблонов
templates = Jinja2Templates(directory="app/templates")
templates.env.globals["now"] = lambda: datetime.now()
templates.env.globals["timedelta"] = timedelta

# Подключение роутеров
app.include_router(companies.router)
app.include_router(employees.router)
app.include_router(tasks.router)
app.include_router(notes.router)

# Подключение статики
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

# Главная страница перенаправляет на список работников
@app.get("/")
async def root():
    return RedirectResponse("/employees")