# Тут буде описана логіка роботи з БД

import sqlite3


async def insert_data(data):
    conn = sqlite3.connect("Schedule.db")
    cursor = conn.cursor()

    email, password = data

    cursor.execute(
        "INSERT OR IGNORE INTO users (email, password) VALUES (?, ?)", (email, password)
    )
    # data = cursor.fetchone()

    if cursor.rowcount == 1:
        data = "Реєстрація успішна"
    else:
        data = "Користувач вже інсує"

    conn.commit()
    conn.close()

    return data


async def search_data(data):

    conn = sqlite3.connect("Schedule.db")
    cursor = conn.cursor()
    email, password = data

    cursor.execute("SELECT id, email, password FROM users WHERE email = ? ", (email,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        id, email, password = result
        return email, password
    else:
        return None, None
