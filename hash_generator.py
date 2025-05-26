import bcrypt

# Укажи пароль
password = "05031991!"

# Генерация хеша
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Вывод результата
print(hashed.decode())