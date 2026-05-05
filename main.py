import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("900x600")
        
        # Данные тренировок
        self.workouts = []
        self.filename = "workouts.json"
        
        # Цветовая схема
        self.colors = {
            'bg': '#f0f0f0',
            'button': '#4CAF50',
            'button_text': 'white',
            'header': '#2196F3',
            'error': '#f44336'
        }
        
        # Настройка стилей
        self.setup_styles()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Загрузка данных
        self.load_data()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Стиль для кнопок
        style.configure('Add.TButton', 
                       background=self.colors['button'],
                       foreground=self.colors['button_text'],
                       padding=10)
        
    def create_widgets(self):
        # Главный контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Форма ввода
        self.create_input_form(main_frame)
        
        # Фильтры
        self.create_filters(main_frame)
        
        # Таблица тренировок
        self.create_table(main_frame)
        
        # Кнопки управления
        self.create_buttons(main_frame)
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                               relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
    def create_input_form(self, parent):
        # Фрейм для формы ввода
        input_frame = ttk.LabelFrame(parent, text="Добавление тренировки", padding="10")
        input_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Дата
        ttk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(input_frame, textvariable=self.date_var, width=15)
        self.date_entry.grid(row=0, column=1, padx=5)
        
        # Тип тренировки
        ttk.Label(input_frame, text="Тип тренировки:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.type_var = tk.StringVar()
        workout_types = ["Бег", "Силовая", "Кардио", "Йога", "Плавание", "Растяжка", "Велосипед", "Другое"]
        self.type_combo = ttk.Combobox(input_frame, textvariable=self.type_var, 
                                       values=workout_types, width=15)
        self.type_combo.grid(row=0, column=3, padx=5)
        self.type_combo.set("Бег")
        
        # Длительность
        ttk.Label(input_frame, text="Длительность (мин):").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.duration_var = tk.StringVar()
        self.duration_entry = ttk.Entry(input_frame, textvariable=self.duration_var, width=10)
        self.duration_entry.grid(row=0, column=5, padx=5)
        
        # Кнопка добавления
        add_button = tk.Button(input_frame, text="+ Добавить тренировку", 
                              command=self.add_workout,
                              bg=self.colors['button'], 
                              fg=self.colors['button_text'],
                              font=('Arial', 10, 'bold'),
                              padx=20, pady=5)
        add_button.grid(row=0, column=6, padx=20)
        
    def create_filters(self, parent):
        # Фрейм для фильтров
        filter_frame = ttk.LabelFrame(parent, text="Фильтры", padding="10")
        filter_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Фильтр по типу
        ttk.Label(filter_frame, text="Тип тренировки:").grid(row=0, column=0, padx=5)
        self.filter_type_var = tk.StringVar(value="Все")
        filter_types = ["Все", "Бег", "Силовая", "Кардио", "Йога", "Плавание", "Растяжка", "Велосипед", "Другое"]
        self.filter_type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type_var,
                                              values=filter_types, width=15)
        self.filter_type_combo.grid(row=0, column=1, padx=5)
        
        # Фильтр по дате
        ttk.Label(filter_frame, text="Дата с:").grid(row=0, column=2, padx=5)
        self.filter_date_from_var = tk.StringVar()
        self.filter_date_from = ttk.Entry(filter_frame, textvariable=self.filter_date_from_var, width=12)
        self.filter_date_from.grid(row=0, column=3, padx=5)
        
        ttk.Label(filter_frame, text="по:").grid(row=0, column=4, padx=5)
        self.filter_date_to_var = tk.StringVar()
        self.filter_date_to = ttk.Entry(filter_frame, textvariable=self.filter_date_to_var, width=12)
        self.filter_date_to.grid(row=0, column=5, padx=5)
        
        # Кнопки фильтрации
        apply_filter_btn = tk.Button(filter_frame, text="Применить фильтр",
                                    command=self.apply_filters,
                                    bg=self.colors['header'],
                                    fg='white',
                                    padx=10, pady=3)
        apply_filter_btn.grid(row=0, column=6, padx=5)
        
        clear_filter_btn = tk.Button(filter_frame, text="Сбросить",
                                    command=self.clear_filters,
                                    padx=10, pady=3)
        clear_filter_btn.grid(row=0, column=7, padx=5)
        
    def create_table(self, parent):
        # Фрейм для таблицы
        table_frame = ttk.LabelFrame(parent, text="Список тренировок", padding="10")
        table_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Создание Treeview
        columns = ('date', 'type', 'duration')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)
        
        # Определение заголовков
        self.tree.heading('date', text='Дата')
        self.tree.heading('type', text='Тип тренировки')
        self.tree.heading('duration', text='Длительность (мин)')
        
        # Ширина колонок
        self.tree.column('date', width=120)
        self.tree.column('type', width=150)
        self.tree.column('duration', width=120)
        
        # Добавление scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещение таблицы и scrollbar
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Привязка двойного клика для удаления
        self.tree.bind('<Double-1>', self.delete_selected)
        
        # Настройка веса для растягивания
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
    def create_buttons(self, parent):
        # Фрейм для кнопок управления
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        save_button = tk.Button(button_frame, text="💾 Сохранить",
                               command=self.save_data,
                               padx=15, pady=5)
        save_button.pack(side=tk.LEFT, padx=5)
        
        load_button = tk.Button(button_frame, text="📂 Загрузить",
                               command=self.load_data,
                               padx=15, pady=5)
        load_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = tk.Button(button_frame, text="🗑️ Очистить все",
                                command=self.clear_all,
                                padx=15, pady=5,
                                bg=self.colors['error'],
                                fg='white')
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Статистика
        self.stats_label = ttk.Label(button_frame, text="", font=('Arial', 9))
        self.stats_label.pack(side=tk.RIGHT, padx=10)
        
    def validate_date(self, date_str):
        """Проверка формата даты"""
        try:
            datetime.strptime(date_str, '%d.%m.%Y')
            return True
        except ValueError:
            return False
    
    def validate_duration(self, duration_str):
        """Проверка длительности"""
        try:
            duration = int(duration_str)
            return duration > 0
        except ValueError:
            return False
    
    def add_workout(self):
        """Добавление новой тренировки"""
        date = self.date_var.get().strip()
        workout_type = self.type_var.get().strip()
        duration = self.duration_var.get().strip()
        
        # Проверка заполнения полей
        if not date or not workout_type or not duration:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return
        
        # Проверка даты
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ДД.ММ.ГГГГ")
            return
        
        # Проверка длительности
        if not self.validate_duration(duration):
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом!")
            return
        
        # Добавление записи
        workout = {
            'date': date,
            'type': workout_type,
            'duration': int(duration)
        }
        
        self.workouts.append(workout)
        
        # Обновление отображения
        self.refresh_table()
        self.update_stats()
        
        # Очистка полей
        self.clear_input_fields()
        
        # Автосохранение
        self.save_data(silent=True)
        
        self.status_var.set(f"Добавлена тренировка: {workout_type} ({date})")
        
    def clear_input_fields(self):
        """Очистка полей ввода"""
        self.date_var.set("")
        self.duration_var.set("")
        self.date_entry.focus()
        
    def refresh_table(self, workouts=None):
        """Обновление таблицы"""
        # Очистка текущих записей
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавление записей
        data = workouts if workouts is not None else self.workouts
        for workout in data:
            self.tree.insert('', tk.END, values=(
                workout['date'],
                workout['type'],
                workout['duration']
            ))
            
    def apply_filters(self):
        """Применение фильтров"""
        filtered_workouts = self.workouts.copy()
        
        # Фильтр по типу
        filter_type = self.filter_type_var.get()
        if filter_type and filter_type != "Все":
            filtered_workouts = [w for w in filtered_workouts if w['type'] == filter_type]
        
        # Фильтр по дате
        date_from = self.filter_date_from_var.get().strip()
        date_to = self.filter_date_to_var.get().strip()
        
        if date_from:
            if not self.validate_date(date_from):
                messagebox.showerror("Ошибка", "Неверный формат даты начала!")
                return
            from_date = datetime.strptime(date_from, '%d.%m.%Y')
            filtered_workouts = [w for w in filtered_workouts 
                               if datetime.strptime(w['date'], '%d.%m.%Y') >= from_date]
        
        if date_to:
            if not self.validate_date(date_to):
                messagebox.showerror("Ошибка", "Неверный формат даты окончания!")
                return
            to_date = datetime.strptime(date_to, '%d.%m.%Y')
            filtered_workouts = [w for w in filtered_workouts 
                               if datetime.strptime(w['date'], '%d.%m.%Y') <= to_date]
        
        # Обновление таблицы
        self.refresh_table(filtered_workouts)
        self.status_var.set(f"Показано {len(filtered_workouts)} записей")
        
    def clear_filters(self):
        """Сброс фильтров"""
        self.filter_type_var.set("Все")
        self.filter_date_from_var.set("")
        self.filter_date_to_var.set("")
        self.refresh_table()
        self.update_stats()
        self.status_var.set("Фильтры сброшены")
        
    def delete_selected(self, event):
        """Удаление выбранной записи"""
        selected = self.tree.selection()
        if not selected:
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранную тренировку?"):
            item = self.tree.item(selected[0])
            values = item['values']
            
            # Поиск и удаление из списка
            for workout in self.workouts:
                if (workout['date'] == values[0] and 
                    workout['type'] == values[1] and 
                    workout['duration'] == int(values[2])):
                    self.workouts.remove(workout)
                    break
            
            self.refresh_table()
            self.update_stats()
            self.save_data(silent=True)
            self.status_var.set("Запись удалена")
    
    def clear_all(self):
        """Очистка всех записей"""
        if messagebox.askyesno("Подтверждение", "Удалить ВСЕ записи?"):
            self.workouts.clear()
            self.refresh_table()
            self.update_stats()
            self.status_var.set("Все записи удалены")
    
    def update_stats(self):
        """Обновление статистики"""
        total = len(self.workouts)
        if total > 0:
            total_duration = sum(w['duration'] for w in self.workouts)
            avg_duration = total_duration / total
            self.stats_label.config(
                text=f"Всего тренировок: {total} | "
                     f"Общая длительность: {total_duration} мин | "
                     f"Средняя: {avg_duration:.1f} мин"
            )
        else:
            self.stats_label.config(text="Нет данных")
    
    def save_data(self, silent=False):
        """Сохранение данных в JSON"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.workouts, file, ensure_ascii=False, indent=4)
            if not silent:
                self.status_var.set(f"Данные сохранены в {self.filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")
    
    def load_data(self):
        """Загрузка данных из JSON"""
        if not os.path.exists(self.filename):
            return
            
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.workouts = json.load(file)
            self.refresh_table()
            self.update_stats()
            self.status_var.set(f"Данные загружены из {self.filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")

def main():
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()

if __name__ == "__main__":
    main()
