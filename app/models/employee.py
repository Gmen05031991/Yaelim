from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.document import Document
from app.models.company import Company  # 💡 ВАЖНО
from datetime import datetime



class Employee(Base):
    __tablename__ = "employees"
    

    id = Column(Integer, primary_key=True, index=True)
    internal_id = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    birth_date = Column(Date)
    passport_number = Column(String)
    visa_expiry = Column(Date)
    address = Column(String)
    status = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"))
    
    notes = relationship("Note", back_populates="employee", cascade="all, delete-orphan")


    documents = relationship(Document, back_populates="employee")
    company = relationship(Company, back_populates="employees")  # 💡 ЭТА СТРОКА ОБЯЗАТЕЛЬНА
    tasks = relationship("Task", back_populates="employee", cascade="all, delete")