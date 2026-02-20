import requests, json, os, tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Курсы валют")
        self.data = None
        self.groups = {}

        tk.Label(root, text="Ввод (код валюты / название группы):").pack(pady=5)
        self.input = tk.Entry(root, width=50)
        self.input.pack(pady=2)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        buttons = [
            ("Все валюты", self.show_all),
            ("Найти", self.find),
            ("Создать группу", self.create_group),
            ("Добавить в группу", self.add_to_group),
            ("Удалить из группы", self.remove_from_group),
        ]
        for i, (txt, cmd) in enumerate(buttons):
            tk.Button(btn_frame, text=txt, command=cmd).grid(row=0, column=i, padx=2)

        btn_frame2 = tk.Frame(root)
        btn_frame2.pack(pady=5)

        buttons2 = [
            ("Сохранить", self.save),
            ("Загрузить", self.load),
            ("Обновить курсы", self.fetch),
            ("Показать группы", self.show_groups),
            ("Выход", root.quit),
        ]
        for i, (txt, cmd) in enumerate(buttons2):
            tk.Button(btn_frame2, text=txt, command=cmd).grid(row=0, column=i, padx=2)

        self.out = tk.Text(root, height=15, width=60)
        self.out.pack(pady=5, padx=10)
        self.load()
        self.fetch()
        self.input.focus()

    def fetch(self):
        try:
            self.data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=10).json()
            self.log("Курсы обновлены")
        except Exception as e:
            self.log(f"Ошибка: {e}")

    def log(self, txt):
        self.out.insert(tk.END, txt + "\n")
        self.out.see(tk.END)

    def clear(self):
        self.out.delete(1.0, tk.END)

    def get_input(self):
        return self.input.get().strip()

    def show_all(self):
        self.clear()
        if not self.data:
            return self.log("Нет данных. Нажмите 'Обновить курсы'")
        for c, v in self.data['Valute'].items():
            self.log(f"{c}: {v['Name']} = {v['Value']} ₽ за {v['Nominal']}")

    def find(self):
        self.clear()
        if not self.data:
            return self.log("Нет данных")
        c = self.get_input().upper()
        if not c:
            return self.log("Введите код валюты")
        v = self.data['Valute'].get(c)
        if v:
            self.log(f"{c}: {v['Name']} = {v['Value']} ₽ за {v['Nominal']}")
        else:
            self.log("Валюта не найдена")

    def create_group(self):
        name = self.get_input()
        if name:
            self.groups.setdefault(name, [])
            self.log(f"Группа '{name}' создана")
        else:
            self.log("Введите название группы")

    def add_to_group(self):
        parts = self.get_input().split()
        if len(parts) != 2:
            return self.log("Формат: КОД ГРУППА (пример: USD моя_группа)")
        c, g = parts[0].upper(), parts[1]
        if g not in self.groups:
            return self.log(f"Группа '{g}' не существует")
        if c in self.groups[g]:
            return self.log("Уже в группе")
        self.groups[g].append(c)
        self.log(f"{c} добавлена в '{g}'")

    def remove_from_group(self):
        parts = self.get_input().split()
        if len(parts) != 2:
            return self.log("Формат: КОД ГРУППА (пример: USD моя_группа)")
        c, g = parts[0], parts[1]
        if g not in self.groups:
            return self.log(f"Группа '{g}' не существует")
        if c not in self.groups[g]:
            return self.log("Нет в группе")
        self.groups[g].remove(c)
        self.log(f"{c} удалена из '{g}'")

    def show_groups(self):
        self.clear()
        if not self.groups:
            return self.log("Групп нет")
        for n, cs in self.groups.items():
            self.log(f"{n}: {', '.join(cs) or 'пусто'}")

    def save(self):
        try:
            os.makedirs('resource', exist_ok=True)
            with open('resource/save.json', 'w', encoding='utf-8') as f:
                json.dump(self.groups, f, ensure_ascii=False, indent=2)
            self.log("Сохранено")
        except Exception as e:
            self.log(f"Ошибка: {e}")

    def load(self):
        try:
            if os.path.exists('resource/save.json'):
                with open('resource/save.json', 'r', encoding='utf-8') as f:
                    self.groups = json.load(f)
                self.log("Группы загружены")
            else:
                self.log("Файл не найден")
            self.groups = self.groups or {}
        except Exception as e:
            self.log(f"Ошибка: {e}")
            self.groups = {}


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()