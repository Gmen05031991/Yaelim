from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import engine, Base
from app.routers import companies
from app.models import employee, company, document, task
from datetime import datetime, timedelta
from app.routers import employees
from app.models import task  # 👈 добавить в import всех моделей
from app.routers import tasks


import os


os.makedirs("app/data", exist_ok=True)
os.makedirs("app/uploads", exist_ok=True)
os.makedirs("app/static/img", exist_ok=True)
os.makedirs("app/templates", exist_ok=True)

app = FastAPI(
    title="Yaelim HR Cloud",
    description="ניהול עובדים עם מסמכים, ויזות ומשימות",
    version="1.0.0",
    debug=True  # ← ДОБАВЬ ЭТУ СТРОКУ
)

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["now"] = lambda: datetime.now()
templates.env.globals["timedelta"] = timedelta

app.include_router(tasks.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# <<< Создание таблиц — после импорта моделей >>>
Base.metadata.create_all(bind=engine)

app.include_router(employees.router)

app.include_router(companies.router)

@app.get("/")
async def root():
    return RedirectResponse("/employees")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
