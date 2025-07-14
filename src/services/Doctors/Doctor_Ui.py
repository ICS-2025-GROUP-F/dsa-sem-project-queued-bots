# doctor_appointment_ui.py

# After
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../patient')))



import tkinter as tk
from tkinter import messagebox
import doctors_LL
import patient_queue
from doctors_LL import *
# Init DB access (forces import)
doctors_LL.get_all_doctors
patient_queue.get_all_patients

# Create UI
root = tk.Tk()
root.title("Doctor Appointment Scheduler")

# --- Doctor Entry Form ---
tk.Label(root, text="Doctor ID").grid(row=0, column=0)
entry_doc_id = tk.Entry(root)
entry_doc_id.grid(row=0, column=1)

tk.Label(root, text="Doctor Name").grid(row=1, column=0)
entry_doc_name = tk.Entry(root)
entry_doc_name.grid(row=1, column=1)

tk.Label(root, text="Specialty").grid(row=2, column=0)
entry_specialty = tk.Entry(root)
entry_specialty.grid(row=2, column=1)

# --- Add Doctor Button ---
def add_doctor():
    doc_id = entry_doc_id.get().strip()
    name = entry_doc_name.get().strip()
    specialty = entry_specialty.get().strip()

    if not doc_id or not name:
        messagebox.showwarning("Missing Info", "Enter Doctor ID and Name.")
        return

    doctors_LL.add_doctor(doc_id, name, specialty)
    update_doctor_list()
    entry_doc_id.delete(0, 'end')
    entry_doc_name.delete(0, 'end')
    entry_specialty.delete(0, 'end')

tk.Button(root, text="Add Doctor", command=add_doctor).grid(row=3, column=0, columnspan=2, pady=10)

# --- Doctor and Patient Selection ---
tk.Label(root, text="Select Doctor").grid(row=4, column=0)
doctor_var = tk.StringVar()
doctor_menu = tk.OptionMenu(root, doctor_var, "")
doctor_menu.grid(row=4, column=1, sticky="ew")

tk.Label(root, text="Select Patient").grid(row=5, column=0)
patient_var = tk.StringVar()
patient_menu = tk.OptionMenu(root, patient_var, "")
patient_menu.grid(row=5, column=1, sticky="ew")

# --- Add Appointment ---
def add_appointment():
    try:
        doc_id = doctor_var.get().split(" - ")[0]
        pat_id = patient_var.get().split(" - ")[0]
        print(f"[UI] Add Appointment clicked. Doctor ID: {doc_id}, Patient ID: {pat_id}")
    except IndexError:
        messagebox.showwarning("Selection Error", "Select both a doctor and patient.")
        return

    doctors_LL.add_appointment(doc_id, pat_id)
    update_appointment_list()


tk.Button(root, text="Add Appointment", command=add_appointment).grid(row=6, column=0, pady=10)

# --- Remove Appointment ---
def remove_appointment():
    try:
        doc_id = doctor_var.get().split(" - ")[0]
        pat_id = patient_var.get().split(" - ")[0]
    except IndexError:
        messagebox.showwarning("Selection Error", "Select both a doctor and patient.")
        return

    doctors_LL.remove_appointment(doc_id, pat_id)
    update_appointment_list()

tk.Button(root, text="Remove Appointment", command=remove_appointment).grid(row=6, column=1, pady=10)

# --- Appointment List ---
tk.Label(root, text="Appointments").grid(row=7, column=0, columnspan=2)
appointment_listbox = tk.Listbox(root, width=50)
appointment_listbox.grid(row=8, column=0, columnspan=2, pady=5)

def update_doctor_list():
    doctors = doctors_LL.get_all_doctors()
    menu = doctor_menu["menu"]
    menu.delete(0, "end")
    for doc in doctors:
        display = f"{doc[0]} - {doc[1]}"
        menu.add_command(label=display, command=lambda value=display: doctor_var.set(value))
    if doctors:
        doctor_var.set(f"{doctors[0][0]} - {doctors[0][1]}")
        update_appointment_list()

def update_patient_list():
    patients = patient_queue.get_all_patients()
    menu = patient_menu["menu"]
    menu.delete(0, "end")
    for pat in patients:
        display = f"{pat[0]} - {pat[1]}"
        menu.add_command(label=display, command=lambda value=display: patient_var.set(value))
    if patients:
        patient_var.set(f"{patients[0][0]} - {patients[0][1]}")

def update_appointment_list():
    appointment_listbox.delete(0, 'end')
    try:
        doc_id = doctor_var.get().split(" - ")[0]
    except IndexError:
        return

    appointments = doctors_LL.get_appointments_for_doctor(doc_id)
    all_patients = {p[0]: p[1] for p in patient_queue.get_all_patients()}
    for pid in appointments:
        name = all_patients.get(pid, "Unknown")
        appointment_listbox.insert('end', f"{name} (ID: {pid})")

# Initial load
update_doctor_list()
update_patient_list()

root.mainloop()
