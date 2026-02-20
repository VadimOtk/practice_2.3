import tkinter as tk
import requests

def check_url_status(url):
    try:
        response = requests.get(url)
        code = response.status_code
        if code in [200, 201, 202, 204, 301, 302, 304]:
            status = "доступен"
        elif code == 403:
            status = "вход запрещен"
        elif code in [404, 410]:
            status = "не найден"
        else:
            status = "не доступен"

        return f"{code} – {status}"

    except requests.RequestException:
        return "ошибка подключения – не доступен"

def check():
    for url in urls:
        result = check_url_status(url.strip())
        text.insert(tk.END, f"{url.strip()} – {result}\n")

root = tk.Tk()
root.title("Проверка URL")
root.geometry("500x300")

text = tk.Text(root, width=60, height=15)
text.pack(padx=10, pady=10)

urls = [
    "https://github.com/",
    "https://www.binance.com/en",
    "https://tomtit.tomsk.ru/",
    "https://jsonplaceholder.typicode.com/",
    "https://moodle.tomtit-tomsk.ru/"
]

check()

root.mainloop()