from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import note, employee
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

router = APIRouter()

@router.post("/employees/{employee_id}/add_note")
def add_note(employee_id: int, content: str = Form(...), db: Session = Depends(get_db)):
    new_note = note.Note(content=content, employee_id=employee_id)
    db.add(new_note)
    db.commit()
    return RedirectResponse(url=f"/employees/{employee_id}", status_code=HTTP_303_SEE_OTHER)
