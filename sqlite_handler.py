import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

def create_tables():
    cur.execute('''CREATE TABLE if not exists "Pacientes" (
	"name"	TEXT NOT NULL,
	"age"	INTEGER NOT NULL,
	"gender"	TEXT NOT NULL,
	"id"	TEXT NOT NULL UNIQUE,
	"phone_number"	TEXT NOT NULL,
    "register_date" TEXT NOT NULL
);''')
    cur.execute(''' CREATE TABLE if not exists "Appointments" (
	"id"	TEXT NOT NULL,
	"problem_description"	TEXT NOT NULL,
	"date"	TEXT NOT NULL,
	"location"	TEXT NOT NULL
);
    ''')
    con.commit()

def create_new_patient(name, age, gender, id, phone_number, register_date):
    cur.execute('''INSERT INTO "Pacientes" 
    ("name", "age", "gender", "id", "phone_number", "register_date") 
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, age, gender, id , phone_number, register_date))
    con.commit()

def create_new_appointment(id, problem_description, date, location):
    cur.execute('''INSERT INTO "Appointments"
    ("id", "problem_description", "date", "location") VALUES 
    (?, ?, ?, ?)
    ''', (id, problem_description, date, location))
    con.commit()

def is_registered(id):
    cur.execute('''SELECT EXISTS(SELECT 1 FROM "Pacientes" WHERE id=?)''', (id,))
    if cur.fetchone()[0] == 1:
        return True
    else:
        return False

def get_data_by_id(id):
    if not is_registered(id):
        print("Patient not registered.")
        return
    cur.execute('''SELECT * from "Pacientes" where id=?
    ''', (id,) )
    return cur.fetchall()[0]

def get_appointments_from_id(id):
    cur.execute('''SELECT * from "Appointments" where id = ?
    ''', (id,))
    return cur.fetchall()

