import tkinter as tk
from tkinter import messagebox
import csv
import os

CONTACTS_FILE = "contacts.csv"

def init_csv():
    if not os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Phone", "Email"])

def add_contact():
    name = name_var.get()
    phone = phone_var.get()
    email = email_var.get()

    if not name or not phone or not email:
        messagebox.showwarning("Warning", "All fields must be filled!")
        return

    with open(CONTACTS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, phone, email])

    clear_fields()
    messagebox.showinfo("Success", "Contact added successfully!")
    view_contacts()

def view_contacts():
    contacts_listbox.delete(0, tk.END)
    with open(CONTACTS_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            contacts_listbox.insert(tk.END, f"Name: {row[0]}, Phone: {row[1]}, Email: {row[2]}")

def delete_contact():
    selected_contact = contacts_listbox.get(tk.ACTIVE)
    if not selected_contact:
        messagebox.showwarning("Warning", "Please select a contact to delete!")
        return

    name = selected_contact.split(",")[0].split(":")[1].strip()

    updated_contacts = []
    with open(CONTACTS_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        updated_contacts = [row for row in reader if row[0] != name]

    with open(CONTACTS_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email"])
        writer.writerows(updated_contacts)

    messagebox.showinfo("Success", "Contact deleted successfully!")
    clear_fields()
    view_contacts()

def update_contact():
    selected_contact = contacts_listbox.get(tk.ACTIVE)
    if not selected_contact:
        messagebox.showwarning("Warning", "Please select a contact to update!")
        return

    name = selected_contact.split(",")[0].split(":")[1].strip()
    phone = phone_var.get()
    email = email_var.get()

    if not phone or not email:
        messagebox.showwarning("Warning", "Phone and Email must be filled for update!")
        return

    updated_contacts = []
    with open(CONTACTS_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0] == name:
                updated_contacts.append([name, phone, email])
            else:
                updated_contacts.append(row)

    with open(CONTACTS_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email"])
        writer.writerows(updated_contacts)

    messagebox.showinfo("Success", "Contact updated successfully!")
    clear_fields()
    view_contacts()

def on_contact_select(event):
    try:
        selected = contacts_listbox.get(contacts_listbox.curselection())
        name, phone, email = [item.split(":")[1].strip() for item in selected.split(",")]
        name_var.set(name)
        phone_var.set(phone)
        email_var.set(email)
    except:
        pass

def clear_fields():
    name_var.set("")
    phone_var.set("")
    email_var.set("")

# Initialize CSV
init_csv()

# GUI Setup
window = tk.Tk()
window.title("Contact Book")
window.geometry("400x500")

# Variables
name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()

# UI Layout
tk.Label(window, text="Name").pack(pady=(10, 0))
tk.Entry(window, textvariable=name_var, width=40).pack()

tk.Label(window, text="Phone").pack(pady=(10, 0))
tk.Entry(window, textvariable=phone_var, width=40).pack()

tk.Label(window, text="Email").pack(pady=(10, 0))
tk.Entry(window, textvariable=email_var, width=40).pack()

tk.Button(window, text="Add Contact", command=add_contact, width=25).pack(pady=5)
tk.Button(window, text="Update Contact", command=update_contact, width=25).pack(pady=5)
tk.Button(window, text="Delete Contact", command=delete_contact, width=25).pack(pady=5)

tk.Label(window, text="Contacts List").pack(pady=(10, 0))
contacts_listbox = tk.Listbox(window, width=50)
contacts_listbox.pack(pady=5)
contacts_listbox.bind("<<ListboxSelect>>", on_contact_select)

# Load contacts on startup
view_contacts()

window.mainloop()
