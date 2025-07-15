# patient_queue_db.py

import sqlite3
import os
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../db/hospital.db'))

# Use DB_PATH in all sqlite3.connect calls:
conn = sqlite3.connect(DB_PATH)
print("Using database at:", DB_PATH)

DB_NAME = 'hospital.db'



def enqueue_patient(patient_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO queue (patient_id) VALUES (?)', (patient_id,))
    conn.commit()
    conn.close()

def dequeue_patient():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, patient_id FROM queue ORDER BY id LIMIT 1')
    row = cursor.fetchone()

    if row:
        queue_id, patient_id = row
        cursor.execute('DELETE FROM queue WHERE id = ?', (queue_id,))
        conn.commit()
        conn.close()
        return patient_id
    conn.close()
    return None

def get_queued_patients():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, p.name, p.age, p.gender
        FROM queue q
        JOIN patients p ON q.patient_id = p.id
        ORDER BY q.id
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_patient_to_db(pid, name, age, gender):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO patients (id, name, age, gender)
        VALUES (?, ?, ?, ?)
    ''', (pid, name, age, gender))
    conn.commit()
    conn.close()

def get_all_patients():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, gender FROM patients")
    rows = cursor.fetchall()
    conn.close()
    return rows