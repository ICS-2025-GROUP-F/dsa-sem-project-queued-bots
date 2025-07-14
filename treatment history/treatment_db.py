import sqlite3
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../db/hospital.db'))

def get_connection():
    return sqlite3.connect(DB_PATH)

print("Resolved DB path:", DB_PATH)
print("[✔] Looking for DB at:", DB_PATH)
print("[✔] DB file exists:", os.path.exists(DB_PATH))


def add_treatment(pid, treatment):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO treatments (patient_id, treatment) VALUES (?, ?)', (pid, treatment))
    conn.commit()
    conn.close()

def undo_last_treatment(pid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM treatments WHERE patient_id = ? ORDER BY id DESC LIMIT 1', (pid,))
    row = cursor.fetchone()
    if row:
        cursor.execute('DELETE FROM treatments WHERE id = ?', (row[0],))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def get_treatment_history(pid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT treatment FROM treatments WHERE patient_id = ? ORDER BY id DESC', (pid,))
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]
