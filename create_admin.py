import sqlite3
import bcrypt


def create_db():
    conn = sqlite3.connect(r'IMS.db')
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Login(name TEXT PRIMARY KEY, pass TEXT, auth TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS employee(emp_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, gender TEXT, dob TEXT, contact TEXT, doj TEXT, usr_type TEXT, address TEXT, salary TEXT)")

    var_emp_id = '1'
    var_email = ''
    var_gender = 'Male'
    var_dob = ''
    var_contact = ''
    var_doj = ''
    txt_address = ''
    var_salary = ''

    name = 'Admin'
    var_usr_type = 'Admin'
    password = str('admin')
    password_bytes = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password_bytes, salt)

    cursor.execute("Insert into Login(name, pass, auth) values(? , ?, ?)", (
        name,
        hash,
        var_usr_type
    ))

    cursor.execute("Insert into employee(emp_id , name , email , gender , dob , contact , doj , usr_type , address , salary) values(?,?,?,?,?,?,?,?,?,?)", (
        var_emp_id,
        name,
        var_email,
        var_gender,
        var_dob,
        var_contact,
        var_doj,
        var_usr_type,
        txt_address,
        var_salary
    ))

    conn.commit()
    conn.close()


create_db()
