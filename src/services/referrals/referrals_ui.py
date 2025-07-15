# graph = referral_graph.DoctorGraph()
# ``instead of`DoctorGraph()`.
#
# ---
#
# ### ✅ 2. **Updated `referral_ui.py` with full module import**
#
# ```python
# # referral_ui.py

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import referrals_graphs as referral_graph

DB_PATH = '../../db/hospital.db'  # Adjust if needed
graph = referral_graph.DoctorGraph()

def get_doctors():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM doctors")
    doctors = cursor.fetchall()
    conn.close()
    return doctors

def update_doctor_lists():
    doctors = get_doctors()
    name_map.clear()
    from_combo['values'] = []
    to_combo['values'] = []

    for doc_id, name in doctors:
        display_name = f"{name} ({doc_id})"
        name_map[display_name] = doc_id
        from_combo['values'] = (*from_combo['values'], display_name)
        to_combo['values'] = (*to_combo['values'], display_name)

def add_doctor():
    name = entry_name.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Doctor name is required.")
        return

    graph.add_doctor(name)
    entry_name.delete(0, tk.END)
    update_doctor_lists()
    refresh_referral_list()

def add_referral():
    from_doc = from_combo.get()
    to_doc = to_combo.get()

    if not from_doc or not to_doc:
        messagebox.showwarning("Selection Error", "Both doctors must be selected.")
        return

    if from_doc == to_doc:
        messagebox.showwarning("Invalid Referral", "Cannot refer a doctor to themselves.")
        return

    graph.add_referral(name_map[from_doc], name_map[to_doc])
    refresh_referral_list()

def show_most_connected():
    doc_id, count = graph.most_connected_doctor()
    if doc_id:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM doctors WHERE id = ?", (doc_id,))
        result = cursor.fetchone()
        conn.close()
        name = result[0] if result else doc_id
        messagebox.showinfo("Most Connected", f"{name} ({doc_id}) → {count} referrals")
    else:
        messagebox.showinfo("Info", "No doctors found.")

def check_cycles():
    if graph.detect_cycles():
        messagebox.showwarning("Cycle Detected", "A cycle was found in the referral network.")
    else:
        messagebox.showinfo("Cycle Check", "No cycles found.")

def refresh_referral_list():
    listbox.delete(0, tk.END)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT d1.name, d2.name FROM referrals r JOIN doctors d1 ON r.from_doctor_id = d1.id JOIN doctors d2 ON r.to_doctor_id = d2.id")
    for from_name, to_name in cursor.fetchall():
        listbox.insert(tk.END, f"{from_name} → {to_name}")
    conn.close()

# GUI setup
root = tk.Tk()
root.title("Referral Network Between Doctors")

name_map = {}

tk.Label(root, text="➕ Add New Doctor").grid(row=0, column=0, columnspan=2, pady=(10, 0))
tk.Label(root, text="Doctor Name:").grid(row=1, column=0)
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=1, column=1)
tk.Button(root, text="Add Doctor", command=add_doctor).grid(row=1, column=2, padx=10)

tk.Label(root, text="🔄 Create Referral").grid(row=2, column=0, columnspan=2, pady=(10, 0))
tk.Label(root, text="From Doctor:").grid(row=3, column=0)
from_combo = ttk.Combobox(root, width=30, state="readonly")
from_combo.grid(row=3, column=1)

tk.Label(root, text="To Doctor:").grid(row=4, column=0)
to_combo = ttk.Combobox(root, width=30, state="readonly")
to_combo.grid(row=4, column=1)

tk.Button(root, text="Add Referral", command=add_referral).grid(row=3, column=2, rowspan=2, padx=10)

tk.Button(root, text="Show Most Connected", command=show_most_connected).grid(row=5, column=0, columnspan=3, pady=(10, 0))
tk.Button(root, text="Check for Cycles", command=check_cycles).grid(row=6, column=0, columnspan=3)

tk.Label(root, text="📋 Referral Network").grid(row=7, column=0, columnspan=3, pady=(10, 0))
listbox = tk.Listbox(root, width=60)
listbox.grid(row=8, column=0, columnspan=3, pady=(0, 10))

update_doctor_lists()
refresh_referral_list()

root.mainloop()
