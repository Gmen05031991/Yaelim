from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import company as models

router = APIRouter(prefix="/companies", tags=["חברות"])
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
async def company_list(request: Request, db: Session = Depends(get_db)):
    companies = db.query(models.Company).all()
    return templates.TemplateResponse("company_list.html", {"request": request, "companies": companies})

@router.get("/add", response_class=HTMLResponse)
async def company_add_form(request: Request):
    return templates.TemplateResponse("company_add.html", {"request": request})

@router.post("/add")
async def company_add(name: str = Form(...), db: Session = Depends(get_db)):
    new_company = models.Company(name=name)
    db.add(new_company)
    db.commit()
    return RedirectResponse("/companies", status_code=303)

@router.get("/{company_id}/edit", response_class=HTMLResponse)
async def company_edit_form(company_id: int, request: Request, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    return templates.TemplateResponse("company_edit.html", {"request": request, "company": company})

@router.post("/{company_id}/edit")
async def company_edit(company_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    company.name = name
    db.commit()
    return RedirectResponse("/companies", status_code=303)

@router.get("/{company_id}/delete")
async def company_delete(company_id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    db.delete(company)
    db.commit()
    return RedirectResponse("/companies", status_code=303)
