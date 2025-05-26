from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from app.database import get_db
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    employee_id = Column(Integer, ForeignKey("employees.id"))

    employee = relationship("Employee", back_populates="notes")
