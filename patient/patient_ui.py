import tkinter as tk
from tkinter import messagebox, ttk
import patient_queue as pq

# --- Functions ---

def refresh_queue():
    for row in tree.get_children():
        tree.delete(row)
    for patient in pq.get_queued_patients():
        tree.insert('', tk.END, values=patient)

def add_patient():
    try:
        pid = int(entry_id.get())
        name = entry_name.get()
        age = int(entry_age.get())
        gender = gender_var.get()

        if not name or not gender:
            raise ValueError("Name or gender empty")

        pq.add_patient_to_db(pid, name, age, gender)
        messagebox.showinfo("Success", "Patient added.")
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def enqueue():
    try:
        pid = int(entry_enqueue_id.get())
        pq.enqueue_patient(pid)
        messagebox.showinfo("Success", "Patient enqueued.")
        entry_enqueue_id.delete(0, tk.END)
        refresh_queue()
    except Exception as e:
        messagebox.showerror("Error", f"Could not enqueue: {e}")

def dequeue():
    patient_id = pq.dequeue_patient()
    if patient_id:
        messagebox.showinfo("Dequeued", f"Patient ID {patient_id} removed from queue.")
    else:
        messagebox.showinfo("Queue Empty", "No patients in queue.")
    refresh_queue()

# --- UI Setup ---

root = tk.Tk()
root.title("Patient Queue Management")
root.geometry("700x500")

# Frame for Adding Patient
frame_add = tk.LabelFrame(root, text="Add Patient to Database", padx=10, pady=10)
frame_add.pack(fill="x", padx=10, pady=5)

tk.Label(frame_add, text="Patient ID:").grid(row=0, column=0)
entry_id = tk.Entry(frame_add)
entry_id.grid(row=0, column=1)

tk.Label(frame_add, text="Name:").grid(row=0, column=2)
entry_name = tk.Entry(frame_add)
entry_name.grid(row=0, column=3)

tk.Label(frame_add, text="Age:").grid(row=1, column=0)
entry_age = tk.Entry(frame_add)
entry_age.grid(row=1, column=1)

tk.Label(frame_add, text="Gender:").grid(row=1, column=2)
gender_var = tk.StringVar()
gender_menu = ttk.Combobox(frame_add, textvariable=gender_var, values=["Male", "Female", "Other"], state="readonly")
gender_menu.grid(row=1, column=3)

btn_add = tk.Button(frame_add, text="Add Patient", command=add_patient)
btn_add.grid(row=2, column=3, pady=5)

# Frame for Queue Actions
frame_queue = tk.LabelFrame(root, text="Queue Actions", padx=10, pady=10)
frame_queue.pack(fill="x", padx=10, pady=5)

tk.Label(frame_queue, text="Enqueue Patient ID:").grid(row=0, column=0)
entry_enqueue_id = tk.Entry(frame_queue)
entry_enqueue_id.grid(row=0, column=1)

btn_enqueue = tk.Button(frame_queue, text="Enqueue", command=enqueue)
btn_enqueue.grid(row=0, column=2)

btn_dequeue = tk.Button(frame_queue, text="Dequeue", command=dequeue)
btn_dequeue.grid(row=0, column=3)

# Frame for Viewing Queue
frame_list = tk.LabelFrame(root, text="Current Queue", padx=10, pady=10)
frame_list.pack(fill="both", expand=True, padx=10, pady=5)

tree = ttk.Treeview(frame_list, columns=("ID", "Name", "Age", "Gender"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Gender", text="Gender")
tree.pack(fill="both", expand=True)

refresh_queue()

root.mainloop()
