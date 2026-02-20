import tkinter as tk
import psutil

def update():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('C:\\').percent

    text.delete(1.0, tk.END)
    text.insert(tk.END, f"Загрузка CPU: {cpu}%\n")
    text.insert(tk.END, f"Оперативная память: {memory}%\n")
    text.insert(tk.END, f"Загруженность диска: {disk}%\n")
    root.after(2000, update)

root = tk.Tk()
root.title("Мониторинг")
root.geometry("300x150")

text = tk.Text(root, width=35, height=6)
text.pack(padx=10, pady=10)

update()
root.mainloop()