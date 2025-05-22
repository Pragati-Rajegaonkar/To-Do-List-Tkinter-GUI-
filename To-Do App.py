import tkinter as tk
from tkinter import messagebox
import json
import os

tasks = []
dark_mode = False
panel_visible = False

def load_tasks():
    global tasks
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
            update_listbox()

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)
    save_label.config(text="✅ Tasks saved to: tasks.json")

def add_task():
    task = entry.get().strip()
    if task:
        tasks.append({"text": task, "done": False})
        update_listbox()
        entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

def delete_task():
    try:
        index = listbox.curselection()[0]
        del tasks[index]
        update_listbox()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to delete.")

def toggle_done(event):
    try:
        index = listbox.curselection()[0]
        tasks[index]["done"] = not tasks[index]["done"]
        update_listbox()
        save_tasks()
    except IndexError:
        pass

def update_listbox():
    listbox.delete(0, tk.END)
    for task in tasks:
        text = f"[✓] {task['text']}" if task["done"] else task["text"]
        listbox.insert(tk.END, text)

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    bg = "#1e1e1e" if dark_mode else "#f0f0f0"
    fg = "#ffffff" if dark_mode else "#000000"
    entry_bg = "#2c2c2c" if dark_mode else "white"
    listbox_bg = "#2c2c2c" if dark_mode else "white"

    window.configure(bg=bg)
    entry.configure(bg=entry_bg, fg=fg, insertbackground=fg)
    listbox.configure(bg=listbox_bg, fg=fg)
    save_label.configure(bg=bg, fg="#aaa")
    title.configure(bg=bg, fg=fg)
    footer.configure(bg=bg, fg="#aaa")
    for widget in side_panel.winfo_children():
        if isinstance(widget, tk.Button):
            widget.configure(bg="#333333" if dark_mode else "#4CAF50", fg="white")

def view_saved_tasks():
    if not os.path.exists("tasks.json"):
        messagebox.showinfo("Saved Tasks", "No saved file found.")
        return
    with open("tasks.json", "r") as file:
        saved_data = json.load(file)

    if not saved_data:
        messagebox.showinfo("Saved Tasks", "Saved file is empty.")
        return

    task_lines = []
    for task in saved_data:
        status = "✓ Done" if task["done"] else "⏳ Pending"
        task_lines.append(f"- {task['text']} ({status})")

    popup_text = "\n".join(task_lines)
    messagebox.showinfo("📜 Saved Tasks", popup_text)

def load_from_file():
    load_tasks()
    messagebox.showinfo("Loaded", "Tasks loaded from file.")

def export_to_txt():
    if not tasks:
        messagebox.showinfo("Export", "No tasks to export.")
        return
    with open("tasks_export.txt", "w") as f:
        f.write("Your Tasks Export:\n")
        for task in tasks:
            status = "✓ Done" if task["done"] else "⏳ Pending"
            f.write(f"- {task['text']} ({status})\n")
    messagebox.showinfo("Export", "Tasks exported to tasks_export.txt")

def toggle_panel():
    global panel_visible
    if panel_visible:
        side_panel.place_forget()
    else:
        side_panel.place(x=0, y=0, relheight=1, width=180)
    panel_visible = not panel_visible

def hide_panel(event):
    global panel_visible
    # Check if click is outside the panel area (x > 180)
    if panel_visible and event.x > 180:
        side_panel.place_forget()
        panel_visible = False

# --- UI Setup ---
window = tk.Tk()
window.title("📝 To-Do List App")

window_width = 500
window_height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.resizable(False, False)

# --- Top bar with menu ---
top_bar = tk.Frame(window, height=50)
top_bar.pack(fill=tk.X)

menu_button = tk.Button(top_bar, text="☰", font=("Arial", 16), command=toggle_panel)
menu_button.pack(side=tk.LEFT, padx=10)

title = tk.Label(top_bar, text="My To-Do List", font=("Helvetica", 20, "bold"))
title.pack(pady=5)

entry = tk.Entry(window, font=("Helvetica", 14), width=30, bd=2, relief=tk.GROOVE)
entry.pack(pady=10)

save_label = tk.Label(window, text="", font=("Helvetica", 9), fg="#888")
save_label.pack()

listbox = tk.Listbox(window, width=40, height=15, font=("Helvetica", 12), bd=2, relief=tk.GROOVE, selectbackground="#cce7ff")
listbox.pack(pady=15)
listbox.bind('<Double-1>', toggle_done)

footer = tk.Label(window, text="~ Built with Tkinter ~", font=("Helvetica", 10))
footer.pack(side=tk.BOTTOM, pady=10)

# --- Side Panel (Hidden Initially) ---
side_panel = tk.Frame(window, bg="#4CAF50")
side_panel.place_forget()

buttons = [
    ("➕ Add Task", add_task),
    ("🗑️ Delete Task", delete_task),
    ("💾 Save Tasks", save_tasks),
    ("📂 Load Tasks", load_from_file),
    ("📤 Export to TXT", export_to_txt),
    ("📜 View Saved", view_saved_tasks),
    ("🌙 Toggle Dark Mode", toggle_theme)
]

for i, (text, command) in enumerate(buttons):
    btn = tk.Button(side_panel, text=text, font=("Helvetica", 11), padx=5, pady=8, width=18, command=command)
    btn.pack(pady=4)

# --- Final Setup ---
load_tasks()
apply_theme()
window.bind("<Button-1>", hide_panel)
window.mainloop()
