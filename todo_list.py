import tkinter as tk
import customtkinter as ctk
from CTkListbox import *
from tkinter import messagebox
import sqlite3

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("To-Do List")
root.geometry("400x500")

# Center the window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')
center_window(root, 400, 500)   # Call the function to center

bold_font = ctk.CTkFont(weight="bold")

# Connect to SQLite database
connection = sqlite3.connect('todo.db')
cursor = connection.cursor()

# Create table
command1 = """CREATE TABLE IF NOT EXISTS todo (
    id INTEGER PRIMARY KEY, task TEXT NOT NULL)"""
cursor.execute(command1)

def add_task():
    task = entry.get()
    if task:
        cursor.execute("INSERT INTO todo (task) VALUES (?)", (task,))
        connection.commit()
        listbox.insert(tk.END, task)
        entry.delete(0, ctk.END)

def remove_task():
    try:
        task_index = listbox.curselection()  # This now returns an int directly
        task = listbox.get(task_index)
        cursor.execute("DELETE FROM todo WHERE task = ?", (task,))
        connection.commit()
        listbox.delete(task_index)
    except (IndexError, TypeError):
        pass

def clear_all_tasks():
    # Show a confirmation dialog
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?")
    if confirm:
        # Clear the database
        cursor.execute("DELETE FROM todo")
        connection.commit()
        # Clear the listbox
        listbox.delete(0, ctk.END)
        messagebox.showinfo("Success", "All tasks have been deleted.")
    else:
        messagebox.showinfo("Cancelled", "Operation cancelled. No tasks were deleted.")

def load_tasks():
    cursor.execute("SELECT task FROM todo")
    tasks = cursor.fetchall()
    for task in tasks:
        listbox.insert(tk.END, task[0])

# Create GUI elements
frame = ctk.CTkFrame(root)
frame.pack(pady=10, padx=10, fill="both", expand=True)

label = ctk.CTkLabel(frame, text="Enter new task:", font=bold_font)
label.pack(pady=5)

entry = ctk.CTkEntry(frame, font=("Arial", 25), width=300)
entry.pack(pady=5)

add_button = ctk.CTkButton(frame, text="Add Task", command=add_task, font=bold_font)
add_button.pack(pady=5)

remove_button = ctk.CTkButton(frame, text="Remove Task", command=remove_task, font=bold_font)
remove_button.pack(pady=5)

# Add this after the remove_button
clear_button = ctk.CTkButton(frame, text="Clear All", command=clear_all_tasks, 
                             font=bold_font, width=100, height=25,
                             fg_color="red", hover_color="dark red")
clear_button.pack(pady=5)

# Use tk.Listbox instead of CTkListbox
listbox = CTkListbox(frame, width=500)
listbox.pack(fill="both", expand=True, padx=10, pady=10)

# Load existing tasks
load_tasks()

root.mainloop()

# Close the database connection when the application exits
connection.close()