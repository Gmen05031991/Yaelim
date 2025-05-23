# app/routers/tasks.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models.task import Task
from app.models.employee import Employee

router = APIRouter(prefix="/tasks", tags=["משימות"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def list_tasks(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    employees = db.query(Employee).all()
    return templates.TemplateResponse("task_list.html", {"request": request, "tasks": tasks, "employees": employees})


@router.post("/add")
async def add_task(
    title: str = Form(...),
    due_date: str = Form(...),
    status: str = Form(...),
    employee_id: int = Form(...),
    db: Session = Depends(get_db)
):
    task = Task(
        title=title,
        due_date=datetime.strptime(due_date, "%Y-%m-%d").date(),
        status=status,
        employee_id=employee_id
    )
    db.add(task)
    db.commit()
    return RedirectResponse("/tasks", status_code=303)


@router.post("/{task_id}/delete")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return RedirectResponse("/tasks", status_code=303)


@router.post("/{task_id}/edit")
async def edit_task(
    task_id: int,
    title: str = Form(...),
    due_date: str = Form(...),
    status: str = Form(...),
    employee_id: int = Form(...),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.title = title
        task.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        task.status = status
        task.employee_id = employee_id
        db.commit()
    return RedirectResponse("/tasks", status_code=303)
