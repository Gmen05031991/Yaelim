# init_db.py

import os
from app.database import engine
from app.models import task, employee, company, note, document

DB_PATH = "app/data/yaelim.db"

# Удаляем старую БД, если есть
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f"[✓] Удалено: {DB_PATH}")
else:
    print(f"[!] База не найдена по пути: {DB_PATH}")

# Создаем таблицы заново
task.Base.metadata.create_all(bind=engine)
employee.Base.metadata.create_all(bind=engine)
company.Base.metadata.create_all(bind=engine)
note.Base.metadata.create_all(bind=engine)
document.Base.metadata.create_all(bind=engine)

print("[✓] Таблицы успешно созданы!")
