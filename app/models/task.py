from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    due_date = Column(Date)
    status = Column(String)
    employee_id = Column(Integer, ForeignKey("employees.id"))

    employee = relationship("Employee", back_populates="tasks")
