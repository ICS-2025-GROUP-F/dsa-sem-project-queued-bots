import sqlite3
import os
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../db/hospital.db'))

# Use DB_PATH in all sqlite3.connect calls:
conn = sqlite3.connect(DB_PATH)
print("Using database at:", DB_PATH)

DB_NAME = 'hospital.db'

# --- Linked List Node & Class ---
class AppointmentNode:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.next = None

class AppointmentList:
    def __init__(self):
        self.head = None

    def add(self, patient_id):
        new_node = AppointmentNode(patient_id)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def remove(self, patient_id):
        current = self.head
        prev = None
        while current:
            if current.patient_id == patient_id:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.patient_id)
            current = current.next
        return result


# --- DB Functions ---

def add_doctor(doc_id, name, specialty):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO doctors (id, name, specialty)
        VALUES (?, ?, ?)
    ''', (doc_id, name, specialty))
    conn.commit()
    conn.close()

def get_all_doctors():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, specialty FROM doctors')
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_appointment(doctor_id, patient_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO appointments (doctor_id, patient_id)
        VALUES (?, ?)
    ''', (doctor_id, patient_id))
    conn.commit()
    conn.close()

def remove_appointment(doctor_id, patient_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM appointments
        WHERE doctor_id = ? AND patient_id = ?
    ''', (doctor_id, patient_id))
    conn.commit()
    conn.close()

def get_appointments_for_doctor(doctor_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT patient_id FROM appointments
        WHERE doctor_id = ?
        ORDER BY id
    ''', (doctor_id,))
    rows = cursor.fetchall()
    conn.close()

    ll = AppointmentList()
    for (patient_id,) in rows:
        ll.add(patient_id)
    return ll.to_list()

