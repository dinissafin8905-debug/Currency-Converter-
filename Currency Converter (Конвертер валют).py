import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
import requests

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter - Конвертер валют")
        self.root.geometry("1100x750")
        self.root.configure(bg='#1a1a2e')
        
        # API настройки - ВАШ API КЛЮЧ
        self.api_key = "91bd5456aa6e2eb2c1305cf3"  # Ваш API ключ
        self.api_url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/"
        
        # Данные
        self.history = []
        self.currencies = []
        self.current_file = "currency_history.json"
        
        # Загрузка валют и истории
        self.load_currencies()
        self.load_history()
        
        # Создание интерфейса
        self.create_widgets()
        self.update_history_table()
    
    def load_currencies(self):
        """Загрузка списка доступных валют из API"""
        # Начнем с базового списка валют
        self.currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'RUB', 'KZT', 'UAH', 'CAD', 'AUD', 'CHF', 'TRY']
        
        try:
            print("Попытка загрузки валют из API...")
            response = requests.get(f"{self.api_url}USD", timeout=10)
            data = response.json()
            
            if data.get('result') == 'success':
                self.currencies = sorted(data['conversion_rates'].keys())
                print(f"✓ Загружено {len(self.currencies)} валют")
                print(f"✓ API ключ работает корректно")
            else:
                print(f"✗ Ошибка API: {data.get('error-type', 'Неизвестная ошибка')}")
                print("Используем базовый список валют")
        except Exception as e:
            print(f"✗ Ошибка: {e}")
            print("Используем базовый список валют")
    
    def create_widgets(self):
        # Заголовок
        title_frame = tk.Frame(self.root, bg='#1a1a2e')
        title_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(title_frame, text="💱 CURRENCY CONVERTER", 
                font=('Arial', 24, 'bold'), fg='#00d4ff', bg='#1a1a2e').pack()
        
        tk.Label(title_frame, text="Конвертер валют", 
                font=('Arial', 12), fg='#e0e0e0', bg='#1a1a2e').pack()
        
        tk.Label(title_frame, text="© Дидякина Кристина Игоревна, 2026 г.", 
                font=('Arial', 10), fg='#95a5a6', bg='#1a1a2e').pack(pady=5)
        
        # Создаем панели
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Левая панель - конвертация
        left_panel = tk.Frame(main_frame, bg='#1a1a2e')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Правая панель - история и инструкция
        right_panel = tk.Frame(main_frame, bg='#1a1a2e')
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # ===== ЛЕВАЯ ПАНЕЛЬ =====
        # Рамка конвертации
        convert_frame = tk.LabelFrame(left_panel, text=" КОНВЕРТАЦИЯ ВАЛЮТ ", 
                                      font=('Arial', 12, 'bold'), 
                                      fg='#00d4ff', bg='#16213e')
        convert_frame.pack(fill='x', pady=(0, 10), padx=5)
        
        # Контейнер для полей
        fields_frame = tk.Frame(convert_frame, bg='#16213e')
        fields_frame.pack(padx=20, pady=20)
        
        # Из валюты
        tk.Label(fields_frame, text="ИЗ ВАЛЮТЫ:", font=('Arial', 11, 'bold'), 
                fg='#00d4ff', bg='#16213e').grid(row=0, column=0, sticky='w', pady=10)
        self.from_currency = ttk.Combobox(fields_frame, values=self.currencies, width=15, font=('Arial', 12))
        self.from_currency.set('USD')
        self.from_currency.grid(row=0, column=1, padx=10, pady=10)
        
        # В валюту
        tk.Label(fields_frame, text="В ВАЛЮТУ:", font=('Arial', 11, 'bold'), 
                fg='#00d4ff', bg='#16213e').grid(row=1, column=0, sticky='w', pady=10)
        self.to_currency = ttk.Combobox(fields_frame, values=self.currencies, width=15, font=('Arial', 12))
        self.to_currency.set('EUR')
        self.to_currency.grid(row=1, column=1, padx=10, pady=10)
        
        # Сумма
        tk.Label(fields_frame, text="СУММА:", font=('Arial', 11, 'bold'), 
                fg='#00d4ff', bg='#16213e').grid(row=2, column=0, sticky='w', pady=10)
        self.amount_entry = tk.Entry(fields_frame, width=20, font=('Arial', 14), bg='white')
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Результат
        tk.Label(fields_frame, text="РЕЗУЛЬТАТ:", font=('Arial', 11, 'bold'), 
                fg='#00d4ff', bg='#16213e').grid(row=3, column=0, sticky='w', pady=10)
        self.result_label = tk.Label(fields_frame, text="0.00", font=('Arial', 16, 'bold'), 
                                     fg='#00d4ff', bg='#16213e', width=15, relief='ridge')
        self.result_label.grid(row=3, column=1, padx=10, pady=10)
        
        # Кнопка конвертации
        convert_btn = tk.Button(convert_frame, text="🔄 КОНВЕРТИРОВАТЬ", command=self.convert_currency,
                               bg='#00d4ff', fg='#1a1a2e', font=('Arial', 14, 'bold'),
                               padx=20, pady=10, cursor='hand2', relief='raised')
        convert_btn.pack(pady=20)
        
        # Рамка JSON
        json_frame = tk.LabelFrame(left_panel, text=" РАБОТА С JSON ", 
                                   font=('Arial', 12, 'bold'), 
                                   fg='#00d4ff', bg='#16213e')
        json_frame.pack(fill='x', pady=10, padx=5)
        
        # Кнопки JSON
        btn_container = tk.Frame(json_frame, bg='#16213e')
        btn_container.pack(padx=20, pady=15)
        
        buttons = [
            ("💾 СОХРАНИТЬ В JSON", self.save_json, '#0f3460'),
            ("📂 ЗАГРУЗИТЬ ИЗ JSON", self.load_json, '#0f3460'),
            ("📁 СОХРАНИТЬ КАК...", self.save_json_as, '#533483'),
            ("🗑️ ОЧИСТИТЬ ИСТОРИЮ", self.clear_history, '#e94560')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(btn_container, text=text, command=command,
                           bg=color, fg='white', font=('Arial', 10, 'bold'),
                           cursor='hand2', relief='raised', padx=10, pady=8)
            btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky='ew')
        
        btn_container.columnconfigure(0, weight=1)
        btn_container.columnconfigure(1, weight=1)
        
        # Информация о файле
        self.file_info = tk.Label(left_panel, text=f"📄 Файл: {self.current_file}", 
                                  font=('Arial', 9), fg='#95a5a6', bg='#1a1a2e')
        self.file_info.pack(pady=10)
        
        # ===== ПРАВАЯ ПАНЕЛЬ =====
        # История
        history_frame = tk.LabelFrame(right_panel, text=" ИСТОРИЯ КОНВЕРТАЦИЙ ", 
                                      font=('Arial', 12, 'bold'), 
                                      fg='#00d4ff', bg='#16213e')
        history_frame.pack(fill='both', expand=True, pady=(0, 10), padx=5)
        
        # Таблица
        table_frame = tk.Frame(history_frame, bg='#16213e')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('date', 'amount', 'from_curr', 'to_curr', 'result', 'rate')
        self.history_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)
        
        self.history_tree.heading('date', text='📅 ДАТА')
        self.history_tree.heading('amount', text='💵 СУММА')
        self.history_tree.heading('from_curr', text='📤 ИЗ')
        self.history_tree.heading('to_curr', text='📥 В')
        self.history_tree.heading('result', text='🎯 РЕЗУЛЬТАТ')
        self.history_tree.heading('rate', text='📊 КУРС')
        
        self.history_tree.column('date', width=140)
        self.history_tree.column('amount', width=90)
        self.history_tree.column('from_curr', width=70)
        self.history_tree.column('to_curr', width=70)
        self.history_tree.column('result', width=110)
        self.history_tree.column('rate', width=100)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # ===== ИНСТРУКЦИЯ =====
        self.create_instruction_panel(right_panel)
    
    def create_instruction_panel(self, parent):
        """Создание панели инструкции"""
        instr_frame = tk.LabelFrame(parent, text=" ИНСТРУКЦИЯ ", 
                                    font=('Arial', 12, 'bold'), 
                                    fg='#00d4ff', bg='#16213e')
        instr_frame.pack(fill='x', padx=5)
        
        # Создаем текстовый виджет с прокруткой
        text_frame = tk.Frame(instr_frame, bg='#16213e')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.instr_text = tk.Text(text_frame, height=14, width=45,
                                  bg='#16213e', fg='#00d4ff',
                                  font=('Consolas', 9), wrap='word',
                                  relief='flat', borderwidth=0)
        
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.instr_text.yview)
        self.instr_text.configure(yscrollcommand=scrollbar.set)
        
        # Текст инструкции
        instruction = """
═══════════════════════════════════════════════════════════════
                    КАК ПОЛЬЗОВАТЬСЯ
═══════════════════════════════════════════════════════════════

1️⃣  КОНВЕРТАЦИЯ ВАЛЮТ:

   • Выберите ИСХОДНУЮ валюту (Из валюты)
   • Выберите ЦЕЛЕВУЮ валюту (В валюту)
   • Введите СУММУ для конвертации
   • Нажмите "КОНВЕРТИРОВАТЬ"
   • Результат появится под кнопкой

2️⃣  РАБОТА С JSON ФАЙЛАМИ:

   • СОХРАНИТЬ В JSON - сохранить историю
   • ЗАГРУЗИТЬ ИЗ JSON - загрузить историю
   • СОХРАНИТЬ КАК... - сохранить в новый файл
   • ОЧИСТИТЬ ИСТОРИЮ - удалить все записи

3️⃣  ДОСТУПНЫЕ ВАЛЮТЫ:

   Программа поддерживает все основные валюты мира:
   USD, EUR, GBP, JPY, CNY, RUB, KZT, UAH, 
   CAD, AUD, CHF, TRY и многие другие

4️⃣  ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:

   Пример 1: 100 USD → EUR
   Ввод: Сумма = 100, Из = USD, В = EUR
   Результат: примерно 92.50 EUR

   Пример 2: 5000 RUB → KZT
   Ввод: Сумма = 5000, Из = RUB, В = KZT
   Результат: примерно 24250 KZT

   Пример 3: 50 GBP → JPY
   Ввод: Сумма = 50, Из = GBP, В = JPY
   Результат: примерно 9500 JPY

5️⃣  ПРОВЕРКА КОРРЕКТНОСТИ:

   ✓ Сумма должна быть положительным числом
   ✓ Нельзя оставлять поля пустыми
   ✓ При ошибке вы увидите сообщение

6️⃣  АВТОМАТИЧЕСКОЕ СОХРАНЕНИЕ:

   • Каждая конвертация автоматически сохраняется
   • Файл истории: currency_history.json
   • Можно загрузить сохраненную историю

═══════════════════════════════════════════════════════════════
"""
        
        self.instr_text.insert('1.0', instruction)
        self.instr_text.config(state='disabled')
        
        self.instr_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def convert_currency(self):
        """Конвертация валюты"""
        # Проверка суммы
        amount_str = self.amount_entry.get().strip()
        if not amount_str:
            messagebox.showerror("Ошибка", "Введите сумму для конвертации!")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть больше нуля!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число! (например: 100 или 50.5)")
            return
        
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        
        # Если валюты одинаковые
        if from_curr == to_curr:
            result = amount
            rate = 1.0
            self.result_label.config(text=f"{result:.2f} {to_curr}")
            self.add_to_history(amount, from_curr, to_curr, result, rate)
            messagebox.showinfo("Результат", f"{amount} {from_curr} = {result:.2f} {to_curr}")
            return
        
        try:
            # Показываем статус загрузки
            self.result_label.config(text="Загрузка...")
            self.root.update()
            
            # Запрос к API
            url = f"{self.api_url}{from_curr}"
            print(f"Запрос к API: {url}")
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('result') == 'success':
                rate = data['conversion_rates'].get(to_curr)
                if rate:
                    result = amount * rate
                    self.result_label.config(text=f"{result:.2f} {to_curr}")
                    self.add_to_history(amount, from_curr, to_curr, result, rate)
                    
                    messagebox.showinfo("Конвертация выполнена!", 
                        f"{amount:,.2f} {from_curr}\n"
                        f"= {result:,.2f} {to_curr}\n\n"
                        f"Курс: 1 {from_curr} = {rate:.4f} {to_curr}")
                else:
                    self.result_label.config(text="Ошибка")
                    messagebox.showerror("Ошибка", f"Валюта '{to_curr}' не найдена!")
            else:
                error_msg = data.get('error-type', 'Неизвестная ошибка')
                self.result_label.config(text="Ошибка API")
                
                if error_msg == 'invalid-api-key':
                    messagebox.showerror("Ошибка", 
                        "Неверный API ключ!\n"
                        "Проверьте правильность ключа в коде программы.")
                else:
                    messagebox.showerror("Ошибка API", f"Ошибка: {error_msg}")
                
        except requests.exceptions.Timeout:
            self.result_label.config(text="Таймаут")
            messagebox.showerror("Ошибка", "Превышено время ожидания!\nПроверьте интернет-соединение.")
        except requests.exceptions.ConnectionError:
            self.result_label.config(text="Нет сети")
            messagebox.showerror("Ошибка", "Нет подключения к интернету!\nПроверьте соединение.")
        except Exception as e:
            self.result_label.config(text="Ошибка")
            messagebox.showerror("Ошибка", f"Произошла ошибка:\n{str(e)}")
    
    def add_to_history(self, amount, from_curr, to_curr, result, rate):
        """Добавление в историю"""
        record = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'amount': amount,
            'from_curr': from_curr,
            'to_curr': to_curr,
            'result': round(result, 2),
            'rate': round(rate, 4)
        }
        self.history.insert(0, record)  # Добавляем в начало
        self.update_history_table()
        self.save_json()
    
    def update_history_table(self):
        """Обновление таблицы истории"""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        for record in self.history[:100]:  # Показываем последние 100
            self.history_tree.insert('', 'end', values=(
                record['date'],
                f"{record['amount']:,.2f}",
                record['from_curr'],
                record['to_curr'],
                f"{record['result']:,.2f}",
                record['rate']
            ))
    
    def save_json(self):
        """Сохранение в JSON"""
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            self.file_info.config(text=f"📄 Файл: {self.current_file} ✓ Сохранено")
            print(f"Сохранено {len(self.history)} записей")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить!\n{str(e)}")
    
    def save_json_as(self):
        """Сохранить как"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Сохранить историю как"
        )
        if file_path:
            self.current_file = file_path
            self.save_json()
    
    def load_json(self):
        """Загрузка из JSON"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="Загрузить историю"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    if isinstance(loaded, list):
                        self.history = loaded
                        self.current_file = file_path
                        self.update_history_table()
                        self.file_info.config(text=f"📄 Файл: {self.current_file}")
                        messagebox.showinfo("Успех", f"Загружено {len(self.history)} записей")
                    else:
                        messagebox.showerror("Ошибка", "Неверный формат файла!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить!\n{str(e)}")
    
    def load_history(self):
        """Загрузка истории при запуске"""
        if os.path.exists(self.current_file):
            try:
                with open(self.current_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                print(f"Загружено {len(self.history)} записей из истории")
            except:
                self.history = []
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Очистить всю историю?\nЭто действие нельзя отменить!"):
            self.history = []
            self.update_history_table()
            self.save_json()
            messagebox.showinfo("Успех", "История очищена!")


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()
