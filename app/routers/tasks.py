from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

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

# 📌 Просмотр задач
@router.get("/", response_class=HTMLResponse)
async def list_tasks(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    employees = db.query(Employee).all()
    return templates.TemplateResponse("task_list.html", {
        "request": request,
        "tasks": tasks,
        "employees": employees
    })

# 📌 Форма добавления задачи (если используешь отдельную)
@router.get("/add", response_class=HTMLResponse)
async def add_task_form(request: Request, db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return templates.TemplateResponse("task_add.html", {
        "request": request,
        "employees": employees
    })

# ✅ Добавление задачи
@router.post("/add")
async def add_task(
    title: str = Form(...),
    description: str = Form(""),
    due_date: str = Form(...),
    status: str = Form(...),
    employee_id: str = Form(""),
    db: Session = Depends(get_db)
):
    try:
        emp_id = int(employee_id) if employee_id.strip().isdigit() else None
        task = Task(
            title=title,
            description=description.strip(),
            due_date=datetime.strptime(due_date, "%Y-%m-%d").date(),
            status=status,
            employee_id=emp_id
        )
        db.add(task)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"שגיאה בעת יצירת המשימה: {str(e)}")
    return RedirectResponse("/tasks", status_code=303)

# ✅ Удаление задачи
@router.post("/{task_id}/delete")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return RedirectResponse("/tasks", status_code=303)

# ✅ Обновление задачи
@router.post("/{task_id}/edit")
async def update_task(
    task_id: int,
    title: str = Form(...),
    description: str = Form(""),
    due_date: str = Form(...),
    status: str = Form(...),
    employee_id: str = Form(""),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        emp_id = int(employee_id) if employee_id.strip().isdigit() else None

        task.title = title
        task.description = description.strip()
        task.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        task.status = status
        task.employee_id = emp_id

        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"שגיאה בעת עדכון המשימה: {str(e)}")

    return RedirectResponse("/tasks", status_code=303)

# ✅ Форма редактирования
@router.get("/{task_id}/edit", response_class=HTMLResponse)
async def edit_task_form(task_id: int, request: Request, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    employees = db.query(Employee).all()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("task_edit.html", {
        "request": request,
        "task": task,
        "employees": employees
    })
