import requests
import tkinter as tk
from tkinter import ttk, scrolledtext

def get_user_profile(username):
    r = requests.get(f"https://api.github.com/users/{username.strip()}")
    if r.status_code == 200:
        u = r.json()
        return (f"Имя: {u.get('name', '—')}\n"
                f"Ссылка: {u['html_url']}\n"
                f"Репозиториев: {u['public_repos']}\n"
                f"Обсуждений: {u['public_gists']}\n"
                f"Подписок: {u['following']}\n"
                f"Подписчиков: {u['followers']}")
    return "Пользователь не найден"

def get_user_repos(username):
    r = requests.get(f"https://api.github.com/users/{username.strip()}/repos", params={'per_page': 100})
    if r.status_code == 200:
        out = []
        for repo in r.json():
            out.append(f"Название: {repo['name']}\n"
                       f"Ссылка: {repo['html_url']}\n"
                       f"Язык: {repo.get('language', '—')}\n"
                       f"Видимость: {repo['visibility']}\n"
                       f"Ветка: {repo['default_branch']}\n")
        return "\n".join(out) if out else "Репозитории не найдены"
    return "Пользователь не найден"

def search_repos(query):
    r = requests.get("https://api.github.com/search/repositories", params={'q': query.strip(), 'per_page': 100})
    if r.status_code == 200:
        out = [f"{repo['name']} - {repo['html_url']}" for repo in r.json()['items']]
        return "\n".join(out) if out else "Ничего не найдено"
    return "Ошибка поиска"

def make_tab(parent, func, label_text):
    frame = ttk.Frame(parent)
    label = ttk.Label(frame, text=label_text)
    label.pack(pady=5)
    entry = ttk.Entry(frame, width=40)
    entry.pack(pady=5)
    result = scrolledtext.ScrolledText(frame, width=60, height=20, state='disabled')
    result.pack(pady=5)

    def run():
        val = entry.get()
        if not val:
            return
        result.config(state='normal')
        result.delete('1.0', tk.END)
        result.insert(tk.END, func(val))
        result.config(state='disabled')
    ttk.Button(frame, text="Выполнить", command=run).pack(pady=5)
    return frame

def main():
    root = tk.Tk()
    root.title("GitHub")
    tabs = ttk.Notebook(root)
    tabs.pack(expand=True, fill='both', padx=5, pady=5)

    tabs.add(make_tab(tabs, get_user_profile, "Имя пользователя:"), text="Профиль")
    tabs.add(make_tab(tabs, get_user_repos, "Имя пользователя:"), text="Репозитории")
    tabs.add(make_tab(tabs, search_repos, "Поисковый запрос:"), text="Поиск репозиторий")
    root.mainloop()

if __name__ == "__main__":
    main()