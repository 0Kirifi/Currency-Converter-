import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

# Константы
API_KEY = "ВАШ_КЛЮЧ_API"  # Получите на https://exchangerate-api.com
HISTORY_FILE = "history.json"

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("500x500")

        # Список популярных валют
        self.currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY"]

        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        # Поля выбора валют
        tk.Label(self.root, text="Из:").pack(pady=5)
        self.from_val = ttk.Combobox(self.root, values=self.currencies)
        self.from_val.set("USD")
        self.from_val.pack()

        tk.Label(self.root, text="В:").pack(pady=5)
        self.to_val = ttk.Combobox(self.root, values=self.currencies)
        self.to_val.set("RUB")
        self.to_val.pack()

        # Ввод суммы
        tk.Label(self.root, text="Сумма:").pack(pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        # Кнопка
        tk.Button(self.root, text="Конвертировать", command=self.convert).pack(pady=20)

        # Результат
        self.result_label = tk.Label(self.root, text="Результат: -", font=("Arial", 12, "bold"))
        self.result_label.pack()

        # Таблица истории
        tk.Label(self.root, text="История:").pack(pady=10)
        self.history_tree = ttk.Treeview(self.root, columns=("From", "To", "Amount", "Result"), show="headings", height=5)
        self.history_tree.heading("From", text="Из")
        self.history_tree.heading("To", text="В")
        self.history_tree.heading("Amount", text="Сумма")
        self.history_tree.heading("Result", text="Итог")
        self.history_tree.pack(fill="x", padx=10)

    def convert(self):
        from_curr = self.from_val.get()
        to_curr = self.to_val.get()
        amount_str = self.amount_entry.get()

        # Проверка ввода
        try:
            amount = float(amount_str)
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите положительное число")
            return

        # Запрос к API
        try:
            url = f"https://exchangerate-api.com{API_KEY}/pair/{from_curr}/{to_curr}/{amount}"
            response = requests.get(url).json()
            
            if response["result"] == "success":
                result = round(response["conversion_result"], 2)
                self.result_label.config(text=f"Результат: {result} {to_curr}")
                self.save_to_history(from_curr, to_curr, amount, result)
            else:
                messagebox.showerror("API Error", "Не удалось получить курс")
        except Exception as e:
            messagebox.showerror("Error", f"Ошибка сети: {e}")

    def save_to_history(self, f, t, a, r):
        entry = {"from": f, "to": t, "amount": a, "result": r}
        
        # Обновление таблицы
        self.history_tree.insert("", 0, values=(f, t, a, r))
        
        # Сохранение в JSON
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as file:
                history = json.load(file)
        
        history.append(entry)
        with open(HISTORY_FILE, "w") as file:
            json.dump(history[-10:], file) # Храним последние 10 записей

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as file:
                history = json.load(file)
                for item in history:
                    self.history_tree.insert("", "end", values=(item["from"], item["to"], item["amount"], item["result"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()