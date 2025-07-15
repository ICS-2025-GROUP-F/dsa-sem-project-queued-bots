# referral_graph.py

import sqlite3

DB_PATH = '../../db/hospital.db'  # Adjust path as needed

class DoctorGraph:
    def __init__(self):
        self.graph = {}
        self.load_from_db()

    def add_doctor(self, name, doctor_id=None):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        if doctor_id is None:
            doctor_id = name.replace(" ", "_")[:10]
        try:
            cursor.execute("INSERT OR IGNORE INTO doctors (id, name) VALUES (?, ?)", (doctor_id, name))
            conn.commit()
        except:
            pass
        conn.close()

    def add_referral(self, from_doc, to_doc):
        self.add_doctor(from_doc)
        self.add_doctor(to_doc)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Insert referral in DB
        cursor.execute("INSERT INTO referrals (from_doctor_id, to_doctor_id) VALUES (?, ?)", (from_doc, to_doc))
        conn.commit()
        conn.close()

        self.graph.setdefault(from_doc, set()).add(to_doc)

    def load_from_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM doctors")
        for row in cursor.fetchall():
            self.graph[row[0]] = set()

        cursor.execute("SELECT from_doctor_id, to_doctor_id FROM referrals")
        for from_doc, to_doc in cursor.fetchall():
            self.graph.setdefault(from_doc, set()).add(to_doc)

        conn.close()

    def get_referrals(self):
        return self.graph

    def most_connected_doctor(self):
        max_conn = -1
        most_conn_doc = None
        for doctor, refs in self.graph.items():
            if len(refs) > max_conn:
                max_conn = len(refs)
                most_conn_doc = doctor
        return most_conn_doc, max_conn

    def detect_cycles(self):
        visited = set()
        rec_stack = set()

        def dfs(doctor):
            visited.add(doctor)
            rec_stack.add(doctor)
            for neighbor in self.graph.get(doctor, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(doctor)
            return False

        for doctor in self.graph:
            if doctor not in visited:
                if dfs(doctor):
                    return True
        return False
