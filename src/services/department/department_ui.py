import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

#Setting up the db
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../db/hospital.db'))

print("Connecting to DB at:", DB_PATH)


def get_connection():
    return sqlite3.connect(DB_PATH)

def add_department(name, parent_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO departments (name, parent_id) VALUES (?, ?)", (name, parent_id))
    conn.commit()
    conn.close()

def get_all_departments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, parent_id FROM departments")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Tree Construction 
def build_tree():
    treeview.delete(*treeview.get_children())
    department_map = {}
    for dept_id, name, parent_id in get_all_departments():
        department_map[dept_id] = treeview.insert(
            parent=department_map.get(parent_id, ''),  # '' means root
            index='end',
            iid=str(dept_id),
            text=name
        )

# --- UI Setup ---
root = tk.Tk()
root.title("Department Hierarchy")
root.geometry("600x500")

# Frame for form
form_frame = tk.LabelFrame(root, text="Add Department", padx=10, pady=10)
form_frame.pack(fill="x", padx=10, pady=5)

tk.Label(form_frame, text="Department Name:").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(form_frame)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Parent Department:").grid(row=1, column=0, padx=5, pady=5)
parent_var = tk.StringVar()
parent_menu = ttk.Combobox(form_frame, textvariable=parent_var, state="readonly")
parent_menu.grid(row=1, column=1, padx=5, pady=5)

def refresh_parents():
    departments = get_all_departments()
    options = ["None"] + [f"{row[0]} - {row[1]}" for row in departments]
    parent_menu['values'] = options
    if options:
        parent_var.set("None")

def submit_department():
    name = entry_name.get().strip()
    selected = parent_var.get()
    parent_id = None
    if selected != "None":
        try:
            parent_id = int(selected.split(" - ")[0])
        except:
            messagebox.showerror("Invalid selection", "Parent selection not understood.")
            return

    if not name:
        messagebox.showwarning("Missing Input", "Department name is required.")
        return

    add_department(name, parent_id)
    messagebox.showinfo("Success", f"Department '{name}' added.")
    entry_name.delete(0, tk.END)
    refresh_parents()
    build_tree()

tk.Button(form_frame, text="Add Department", command=submit_department).grid(row=2, column=0, columnspan=2, pady=10)

# --- Department Tree ---
tree_frame = tk.LabelFrame(root, text="Department Tree View", padx=10, pady=10)
tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

treeview = ttk.Treeview(tree_frame)
treeview.heading('#0', text='Department Name', anchor='w')
treeview.pack(fill="both", expand=True)

# Initial Load
refresh_parents()
build_tree()

root.mainloop()
