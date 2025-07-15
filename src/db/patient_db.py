# setup_db.py

import sqlite3

def create_tables():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    # Patients Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT
        )
    ''')

    # Queue Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
    ''')

    # Create the doctors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            specialty TEXT
        )
    ''')

    # Create the appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id TEXT NOT NULL,
            patient_id TEXT NOT NULL,
            FOREIGN KEY (doctor_id) REFERENCES doctors(id),
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    ''')


    # Treatments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            treatment TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
    ''')

    # Departments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES departments(id)
        )
    ''')

    # Referrals Table (Doctor → Doctor)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_doctor_id TEXT NOT NULL,
            to_doctor_id TEXT NOT NULL,
            FOREIGN KEY (from_doctor_id) REFERENCES doctors(id),
            FOREIGN KEY (to_doctor_id) REFERENCES doctors(id)
        )
    ''')


    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in DB:", tables)

    print("✅ Database and tables created successfully.")
    # conn.commit()
    # conn.close()

    conn.commit()

    # Query patients table (may be empty if no data yet)
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()



if __name__ == '__main__':
    create_tables()
