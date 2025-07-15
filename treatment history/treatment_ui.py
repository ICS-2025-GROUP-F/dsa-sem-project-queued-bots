import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../patient')))


import tkinter as tk
from tkinter import messagebox, ttk
import treatment_db  # assumes treatment_db.py exists in the same folder or sys.path
import patient_queue as pq  # for loading patient list

# --- Functions ---

def refresh_history():
    history_list.delete(*history_list.get_children())
    try:
        pid = patient_var.get().split(" - ")[0]
        treatments = treatment_db.get_treatment_history(pid)
        for i, treatment in enumerate(reversed(treatments), 1):
            history_list.insert('', tk.END, values=(i, treatment))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load history.\n{e}")

def add_treatment():
    try:
        pid = patient_var.get().split(" - ")[0]
        treatment = entry_treatment.get().strip()

        if not treatment:
            raise ValueError("Treatment cannot be empty")

        treatment_db.add_treatment(pid, treatment)
        messagebox.showinfo("Success", "Treatment added.")
        entry_treatment.delete(0, tk.END)
        refresh_history()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add treatment.\n{e}")

def undo_treatment():
    try:
        pid = patient_var.get().split(" - ")[0]
        result = treatment_db.undo_last_treatment(pid)
        if result:
            messagebox.showinfo("Success", "Last treatment removed.")
        else:
            messagebox.showinfo("Empty", "No treatments to undo.")
        refresh_history()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to undo.\n{e}")

def load_patients():
    try:
        patients = pq.get_all_patients()
        for pat in patients:
            label = f"{pat[0]} - {pat[1]}"
            patient_menu['menu'].add_command(label=label, command=tk._setit(patient_var, label, refresh_history))
        if patients:
            patient_var.set(f"{patients[0][0]} - {patients[0][1]}")
            refresh_history()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load patients.\n{e}")

# --- UI Setup ---

root = tk.Tk()
root.title("Treatment History Tracker (Stack)")
root.geometry("700x500")

# Patient selection
frame_select = tk.LabelFrame(root, text="Select Patient", padx=10, pady=10)
frame_select.pack(fill="x", padx=10, pady=5)

tk.Label(frame_select, text="Patient:").grid(row=0, column=0)
patient_var = tk.StringVar()
patient_menu = tk.OptionMenu(frame_select, patient_var, "")
patient_menu.grid(row=0, column=1, sticky="ew")

# Add treatment
frame_add = tk.LabelFrame(root, text="Add Treatment", padx=10, pady=10)
frame_add.pack(fill="x", padx=10, pady=5)

tk.Label(frame_add, text="Treatment Description:").grid(row=0, column=0)
entry_treatment = tk.Entry(frame_add, width=50)
entry_treatment.grid(row=0, column=1, padx=10)

btn_add = tk.Button(frame_add, text="Add Treatment", command=add_treatment)
btn_add.grid(row=0, column=2, padx=5)

# Undo treatment
btn_undo = tk.Button(frame_add, text="Undo Last Treatment", command=undo_treatment)
btn_undo.grid(row=0, column=3, padx=5)

# Treatment history list
frame_history = tk.LabelFrame(root, text="Treatment History", padx=10, pady=10)
frame_history.pack(fill="both", expand=True, padx=10, pady=5)

history_list = ttk.Treeview(frame_history, columns=("No", "Treatment"), show="headings")
history_list.heading("No", text="No.")
history_list.heading("Treatment", text="Treatment Description")
history_list.column("No", width=50, anchor="center")
history_list.pack(fill="both", expand=True)

load_patients()
root.mainloop()
