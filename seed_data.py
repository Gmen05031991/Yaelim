from datetime import date, timedelta
from app.database import SessionLocal, Base, engine
from app.models.employee import Employee
from app.models.company import Company

# Создание таблиц (на всякий случай)
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Проверяем, существует ли компания
company = db.query(Company).filter(Company.name == "חברת ניסוי").first()
if not company:
    company = Company(name="חברת ניסוי")
    db.add(company)
    db.commit()
    db.refresh(company)

# Добавление сотрудников (без дублей)
for i in range(1, 7):
    internal_id = f"EMP{i:03}"
    exists = db.query(Employee).filter(Employee.internal_id == internal_id).first()
    if exists:
        print(f"⚠️ Сотрудник {internal_id} уже существует — пропущен.")
        continue

    emp = Employee(
        internal_id=internal_id,
        first_name=f"שם{i}",
        last_name=f"כהן{i}",
        phone="050-0000000",
        birth_date=date(1990, 5, 10 + i),
        passport_number=f"A1234567{i}",
        visa_expiry=date.today() + timedelta(days=5 if i % 2 == 0 else 30),
        address="תל אביב",
        status="Работает" if i % 2 == 0 else "Закончил",
        company_id=company.id
        
        
    )
    db.add(emp)

db.commit()
db.close()
print("✅ Тестовые сотрудники добавлены (без дублей).")
