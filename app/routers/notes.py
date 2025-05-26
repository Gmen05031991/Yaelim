from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.note import Note

router = APIRouter(tags=["הערות"])  # без prefix

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{note_id}/delete")
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        employee_id = note.employee_id
        db.delete(note)
        db.commit()
        return RedirectResponse(f"/employees/{employee_id}", status_code=303)
    raise HTTPException(status_code=404, detail="Note not found")
from fastapi import Form

@router.post("/add")
async def add_note(
    request: Request,
    employee_id: int = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    note = Note(employee_id=employee_id, content=content)
    db.add(note)
    db.commit()
    return RedirectResponse(f"/employees/{employee_id}", status_code=303)


@router.post("/employees/{employee_id}/add_note")
async def add_note_with_path(
    employee_id: int,
    request: Request,
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    note = Note(employee_id=employee_id, content=content)
    db.add(note)
    db.commit()
    return RedirectResponse(f"/employees/{employee_id}", status_code=303)
