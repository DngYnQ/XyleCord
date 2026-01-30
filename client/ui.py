import json
import tkinter as tk
from tkinter import ttk

import client
cl = client.tcp('127.0.0.1', 49111)

def get_items():
    return json.loads(cl.get_channels())

root = tk.Tk()
root.title("Connect")
root.geometry("400x280")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", background="#1e1e1e", foreground="#e0e0e0", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11, "bold"))

ttk.Label(root, text="Выбери сервер:").pack(pady=(20, 8))

listbox = tk.Listbox(
    root,
    bg="#2d2d2d",
    fg="#e0e0e0",
    selectbackground="#4a6a8f",
    selectforeground="white",
    font=("Consolas", 11),
    borderwidth=0,
    highlightthickness=0,
    activestyle="none",
    height=8,
)
listbox.pack(padx=30, pady=6, fill="both", expand=True)

items = get_items()
for item in items:
    listbox.insert(tk.END, f"{item['name']} ({item['type']})")

listbox.select_set(0)

connected = False
current_uuid = None

def connect_or_disconnect():
    global connected, current_uuid

    if not connected:
        sel = listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        server = items[idx]
        uuid = server['uuid']

        print(f"→ Подключаемся к {server['name']} ({uuid})")
        cl.connect(uuid)

        connected = True
        current_uuid = uuid
        btn.config(
            text="DISCONNECT",
            bg="#b71c1c",
            activebackground="#7f0000",
        )
        listbox.config(state="disabled")

    else:
        # Отключаемся
        print(f"→ Отключаемся от {current_uuid}")
        try:
            cl.disconnect()
        except AttributeError:
            print("  (cl.disconnect() не реализована)")

        connected = False
        current_uuid = None
        btn.config(
            text="CONNECT",
            bg="#2e7d32",
            activebackground="#1b5e20",
        )

        listbox.config(state="normal")

btn = tk.Button(
    root,
    text="CONNECT",
    bg="#2e7d32",
    fg="white",
    activebackground="#1b5e20",
    activeforeground="white",
    font=("Segoe UI", 11, "bold"),
    relief="flat",
    bd=0,
    padx=30,
    pady=12,
    command=connect_or_disconnect
)
btn.pack(pady=(10, 30))

root.mainloop()