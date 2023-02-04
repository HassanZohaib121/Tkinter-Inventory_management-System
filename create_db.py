import sqlite3


def Create_db():
    conn = sqlite3.connect(r'IMS.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS employee(emp_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, gender TEXT, dob TEXT, contact TEXT, doj TEXT, usr_type TEXT, address TEXT, salary TEXT)")

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, contact TEXT, detail TEXT)")

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS category(CID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS product(barcode INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price TEXT, quantity TEXT, category TEXT, supplier TEXT, status TEXT)")

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Login(name TEXT PRIMARY KEY, pass TEXT, auth TEXT)")

    conn.commit()
    conn.close()


Create_db()
