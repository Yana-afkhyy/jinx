import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
import sys

class TrainingPlanner:
    """
    GUI-приложение для планирования тренировок.
    Позволяет добавлять, фильтровать и управлять тренировками.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner - План тренировок")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Данные тренировок
        self.workouts = []
        self.filtered_workouts = []
        self.data_file = "workouts.json"
        
        # Настройка стилей
        self.setup_styles()
        
        # Создание интерфейса
        self.create_menu()
        self.create_widgets()
        
        # Загрузка данных
        self.load_data()
        
        # Центрирование окна
        self.center_window()
        
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """Настройка визуальных стилей"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Цветовая схема
        self.colors = {
            'primary': '#2196F3',      # Синий
            'success': '#4CAF50',      # Зеленый
            'danger': '#f44336',       # Красный
            'warning': '#FF9800',      # Оранжевый
            'info': '#00BCD4',         # Голубой
            'bg': '#F5F5F5',          # Светло-серый фон
            'text': '#212121',         # Темный текст
            'white': '#FFFFFF'
        }
        
        # Настройка цветов
        self.root.configure(bg=self.colors['bg'])
        
    def create_menu(self):
        """Создание меню приложения"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить", command=lambda: self.save_data(show_message=True), accelerator="Ctrl+S")
        file_menu.add_command(label="Загрузить", command=self.load_data, accelerator="Ctrl+L")
        file_menu.add_separator()
        file_menu.add_command(label="Экспорт в JSON", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Меню Правка
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Очистить все записи", command=self.clear_all)
        edit_menu.add_command(label="Удалить выбранное", command=self.delete_selected_from_button)
        
        # Меню Вид
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Обновить таблицу", command=self.refresh_table)
        view_menu.add_command(label="Сбросить фильтры", command=self.clear_filters)
        
        # Меню Справка
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
        help_menu.add_command(label="Помощь", command=self.show_help)
        
        # Горячие клавиши
        self.root.bind('<Control-s>', lambda e: self.save_data(show_message=True))
        self.root.bind('<Control-l>', lambda e: self.load_data())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        
    def create_widgets(self):
        """Создание всех виджетов интерфейса"""
        # Главный контейнер с отступами
        main_container = ttk.Frame(self.root, padding="15")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        self.create_header(main_container)
        
        # Форма добавления тренировки
        self.create_input_form(main_container)
        
        # Панель фильтров
        self.create_filter_panel(main_container)
        
        # Таблица тренировок
        self.create_table(main_container)
        
        # Панель статистики
        self.create_stats_panel(main_container)
        
        # Статус-бар
        self.create_status_bar()
        
    def create_header(self, parent):
        """Создание заголовка"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(
            header_frame,
            text="🏋️ TRAINING PLANNER",
            font=('Arial', 18, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        )
        title_label.pack(side=tk.LEFT)
        
        date_label = tk.Label(
            header_frame,
            text=f"📅 {datetime.now().strftime('%d.%m.%Y')}",
            font=('Arial', 10),
            bg=self.colors['bg']
        )
        date_label.pack(side=tk.RIGHT)
        
    def create_input_form(self, parent):
        """Создание формы ввода данных"""
        form_frame = ttk.LabelFrame(
            parent,
            text="📝 Добавление новой тренировки",
            padding="15"
        )
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Сетка для формы
        # Первая строка
        row1_frame = ttk.Frame(form_frame)
        row1_frame.pack(fill=tk.X, pady=5)
        
        # Дата
        ttk.Label(row1_frame, text="Дата:", font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(
            row1_frame,
            textvariable=self.date_var,
            width=15,
            font=('Arial', 10)
        )
        self.date_entry.pack(side=tk.LEFT, padx=(0, 15))
        ttk.Label(row1_frame, text="(ДД.ММ.ГГГГ)", font=('Arial', 8), foreground='gray').pack(side=tk.LEFT, padx=(0, 20))
        
        # Тип тренировки
        ttk.Label(row1_frame, text="Тип:", font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.type_var = tk.StringVar()
        workout_types = [
            "Бег", "Ходьба", "Плавание", "Велосипед",
            "Силовая", "Кардио", "Йога", "Пилатес",
            "Растяжка", "Кроссфит", "Танцы", "Бокс",
            "Единоборства", "Командная игра", "Другое"
        ]
        type_combo = ttk.Combobox(
            row1_frame,
            textvariable=self.type_var,
            values=workout_types,
            width=18,
            font=('Arial', 10),
            state='readonly'
        )
        type_combo.pack(side=tk.LEFT, padx=(0, 20))
        type_combo.set("Выберите тип")
        
        # Длительность
        ttk.Label(row1_frame, text="Длительность:", font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.duration_var = tk.StringVar()
        self.duration_entry = ttk.Entry(
            row1_frame,
            textvariable=self.duration_var,
            width=10,
            font=('Arial', 10)
        )
        self.duration_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(row1_frame, text="мин.", font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 15))
        
        # Вторая строка - кнопки
        row2_frame = ttk.Frame(form_frame)
        row2_frame.pack(fill=tk.X, pady=5)
        
        add_button = tk.Button(
            row2_frame,
            text="➕ ДОБАВИТЬ ТРЕНИРОВКУ",
            command=self.add_workout,
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2',
            relief=tk.RAISED,
            borderwidth=2
        )
        add_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = tk.Button(
            row2_frame,
            text="🗑️ Очистить поля",
            command=self.clear_input_fields,
            bg=self.colors['warning'],
            fg=self.colors['white'],
            font=('Arial', 10),
            padx=15,
            pady=8,
            cursor='hand2'
        )
        clear_button.pack(side=tk.LEFT)
        
        # Сегодняшняя дата по умолчанию
        self.date_var.set(datetime.now().strftime('%d.%m.%Y'))
        
    def create_filter_panel(self, parent):
        """Создание панели фильтров"""
        filter_frame = ttk.LabelFrame(
            parent,
            text="🔍 Фильтрация тренировок",
            padding="15"
        )
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        filter_content = ttk.Frame(filter_frame)
        filter_content.pack(fill=tk.X)
        
        # Фильтр по типу
        ttk.Label(filter_content, text="Тип тренировки:", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.filter_type_var = tk.StringVar(value="Все")
        filter_types = ["Все", "Бег", "Ходьба", "Плавание", "Велосипед", "Силовая", "Кардио", "Йога", "Другое"]
        self.filter_type_combo = ttk.Combobox(
            filter_content,
            textvariable=self.filter_type_var,
            values=filter_types,
            width=18,
            font=('Arial', 10),
            state='readonly'
        )
        self.filter_type_combo.grid(row=0, column=1, padx=(0, 20))
        
        # Фильтр по дате
        ttk.Label(filter_content, text="Дата с:", font=('Arial', 10)).grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.filter_date_from_var = tk.StringVar()
        self.filter_date_from_entry = ttk.Entry(
            filter_content,
            textvariable=self.filter_date_from_var,
            width=12,
            font=('Arial', 10)
        )
        self.filter_date_from_entry.grid(row=0, column=3, padx=(0, 5))
        
        ttk.Label(filter_content, text="по:", font=('Arial', 10)).grid(row=0, column=4, padx=(0, 5))
        self.filter_date_to_var = tk.StringVar()
        self.filter_date_to_entry = ttk.Entry(
            filter_content,
            textvariable=self.filter_date_to_var,
            width=12,
            font=('Arial', 10)
        )
        self.filter_date_to_entry.grid(row=0, column=5, padx=(0, 15))
        
        ttk.Label(filter_content, text="(ДД.ММ.ГГГГ)", font=('Arial', 8), foreground='gray').grid(row=0, column=6, padx=(0, 15))
        
        # Кнопки фильтрации
        apply_btn = tk.Button(
            filter_content,
            text="🔍 Применить",
            command=self.apply_filters,
            bg=self.colors['primary'],
            fg=self.colors['white'],
            font=('Arial', 10),
            padx=15,
            pady=5,
            cursor='hand2'
        )
        apply_btn.grid(row=0, column=7, padx=(0, 5))
        
        reset_btn = tk.Button(
            filter_content,
            text="🔄 Сбросить",
            command=self.clear_filters,
            bg=self.colors['info'],
            fg=self.colors['white'],
            font=('Arial', 10),
            padx=15,
            pady=5,
            cursor='hand2'
        )
        reset_btn.grid(row=0, column=8)
        
    def create_table(self, parent):
        """Создание таблицы для отображения тренировок"""
        table_frame = ttk.LabelFrame(
            parent,
            text="📋 Список тренировок",
            padding="10"
        )
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Создание таблицы с прокруткой
        table_scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        table_scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=('number', 'date', 'type', 'duration', 'intensity'),
            show='headings',
            height=12,
            yscrollcommand=table_scroll_y.set,
            xscrollcommand=table_scroll_x.set
        )
        
        table_scroll_y.config(command=self.tree.yview)
        table_scroll_x.config(command=self.tree.xview)
        
        # Определение колонок
        self.tree.heading('number', text='№')
        self.tree.heading('date', text='📅 Дата')
        self.tree.heading('type', text='🏃 Тип тренировки')
        self.tree.heading('duration', text='⏱️ Длительность (мин)')
        self.tree.heading('intensity', text='💪 Интенсивность')
        
        # Настройка ширины колонок
        self.tree.column('number', width=50, anchor=tk.CENTER)
        self.tree.column('date', width=120, anchor=tk.CENTER)
        self.tree.column('type', width=180, anchor=tk.W)
        self.tree.column('duration', width=150, anchor=tk.CENTER)
        self.tree.column('intensity', width=120, anchor=tk.CENTER)
        
        # Размещение таблицы
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        table_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        table_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Контекстное меню для таблицы
        self.create_context_menu()
        
        # Привязка событий
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Delete>', lambda e: self.delete_selected_from_button())
        
    def create_context_menu(self):
        """Создание контекстного меню для таблицы"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Удалить запись", command=self.delete_selected_from_button)
        self.context_menu.add_command(label="Редактировать", command=self.edit_selected)
        self.tree.bind('<Button-3>', self.show_context_menu)
        
    def show_context_menu(self, event):
        """Показать контекстное меню"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
            
    def create_stats_panel(self, parent):
        """Создание панели статистики"""
        stats_frame = ttk.Frame(parent)
        stats_frame.pack(fill=tk.X)
        
        # Статистика
        self.stats_text = tk.StringVar()
        self.stats_text.set("📊 Статистика: Нет данных")
        
        stats_label = tk.Label(
            stats_frame,
            textvariable=self.stats_text,
            font=('Arial', 10, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            anchor=tk.W,
            padx=10,
            pady=5
        )
        stats_label.pack(fill=tk.X)
        
    def create_status_bar(self):
        """Создание статус-бара"""
        self.status_var = tk.StringVar()
        self.status_var.set("✅ Готов к работе")
        
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padx=10,
            pady=5,
            font=('Arial', 9),
            bg='#E0E0E0'
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    # Методы валидации данных
    def validate_date(self, date_str):
        """Проверка корректности формата даты (ДД.ММ.ГГГГ)"""
        if not date_str:
            return False, "Дата не может быть пустой"
            
        try:
            # Проверка формата
            datetime.strptime(date_str, '%d.%m.%Y')
            
            # Дополнительная проверка на корректность даты
            day, month, year = map(int, date_str.split('.'))
            
            if not (1 <= month <= 12):
                return False, "Месяц должен быть от 1 до 12"
                
            if not (1 <= day <= 31):
                return False, "День должен быть от 1 до 31"
                
            if month in [4, 6, 9, 11] and day > 30:
                return False, "В этом месяце максимум 30 дней"
                
            if month == 2:
                # Проверка високосного года
                is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
                max_day = 29 if is_leap else 28
                if day > max_day:
                    return False, f"В феврале {year} года максимум {max_day} дней"
                    
            return True, ""
            
        except ValueError:
            return False, "Неверный формат даты. Используйте: ДД.ММ.ГГГГ"
            
    def validate_duration(self, duration_str):
        """Проверка длительности (положительное число)"""
        if not duration_str:
            return False, "Длительность не может быть пустой"
            
        try:
            duration = int(duration_str)
            if duration <= 0:
                return False, "Длительность должна быть положительным числом"
            if duration > 1440:  # Больше 24 часов
                return False, "Длительность не может превышать 1440 минут (24 часа)"
            return True, ""
        except ValueError:
            return False, "Длительность должна быть целым числом"
            
    def validate_type(self, workout_type):
        """Проверка типа тренировки"""
        if not workout_type or workout_type == "Выберите тип":
            return False, "Необходимо выбрать тип тренировки"
        return True, ""
        
    # Методы работы с данными
    def add_workout(self):
        """Добавление новой тренировки"""
        # Получение данных из формы
        date = self.date_var.get().strip()
        workout_type = self.type_var.get().strip()
        duration = self.duration_var.get().strip()
        
        # Валидация данных
        date_valid, date_error = self.validate_date(date)
        if not date_valid:
            messagebox.showerror("❌ Ошибка даты", date_error)
            self.date_entry.focus()
            return
            
        type_valid, type_error = self.validate_type(workout_type)
        if not type_valid:
            messagebox.showerror("❌ Ошибка типа", type_error)
            return
            
        duration_valid, duration_error = self.validate_duration(duration)
        if not duration_valid:
            messagebox.showerror("❌ Ошибка длительности", duration_error)
            self.duration_entry.focus()
            return
            
        # Создание записи тренировки
        workout = {
            'date': date,
            'type': workout_type,
            'duration': int(duration),
            'intensity': self.calculate_intensity(int(duration)),
            'added_at': datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        }
        
        # Добавление в список
        self.workouts.append(workout)
        
        # Сортировка по дате (новые сверху)
        self.workouts.sort(key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'), reverse=True)
        
        # Обновление интерфейса
        self.refresh_table()
        self.update_statistics()
        self.save_data()
        
        # Очистка формы (кроме даты)
        self.type_var.set("Выберите тип")
        self.duration_var.set("")
        self.duration_entry.focus()
        
        self.status_var.set(f"✅ Добавлена тренировка: {workout_type} - {date} ({duration} мин.)")
        
    def calculate_intensity(self, duration):
        """Расчет интенсивности на основе длительности"""
        if duration <= 20:
            return "Низкая"
        elif duration <= 45:
            return "Средняя"
        elif duration <= 90:
            return "Высокая"
        else:
            return "Экстремальная"
            
    def refresh_table(self, workouts=None):
        """Обновление данных в таблице"""
        # Очистка текущих записей
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Определение источника данных
        data = workouts if workouts is not None else self.workouts
        
        # Добавление записей в таблицу
        for i, workout in enumerate(data, 1):
            # Определение тега для цвета строки
            tag = 'even' if i % 2 == 0 else 'odd'
            
            self.tree.insert('', tk.END, values=(
                i,
                workout['date'],
                workout['type'],
                workout['duration'],
                workout.get('intensity', self.calculate_intensity(workout['duration']))
            ), tags=(tag,))
            
        # Настройка цветов строк
        self.tree.tag_configure('odd', background='#FFFFFF')
        self.tree.tag_configure('even', background='#F5F5F5')
        
    def apply_filters(self):
        """Применение фильтров к данным"""
        filtered = self.workouts.copy()
        filter_applied = False
        
        # Фильтр по типу тренировки
        filter_type = self.filter_type_var.get()
        if filter_type and filter_type != "Все":
            filtered = [w for w in filtered if w['type'] == filter_type]
            filter_applied = True
            
        # Фильтр по диапазону дат
        date_from = self.filter_date_from_var.get().strip()
        date_to = self.filter_date_to_var.get().strip()
        
        if date_from:
            date_valid, error = self.validate_date(date_from)
            if not date_valid:
                messagebox.showerror("❌ Ошибка фильтра", f"Дата 'с': {error}")
                return
            from_date = datetime.strptime(date_from, '%d.%m.%Y')
            filtered = [w for w in filtered 
                       if datetime.strptime(w['date'], '%d.%m.%Y') >= from_date]
            filter_applied = True
            
        if date_to:
            date_valid, error = self.validate_date(date_to)
            if not date_valid:
                messagebox.showerror("❌ Ошибка фильтра", f"Дата 'по': {error}")
                return
            to_date = datetime.strptime(date_to, '%d.%m.%Y')
            filtered = [w for w in filtered 
                       if datetime.strptime(w['date'], '%d.%m.%Y') <= to_date]
            filter_applied = True
            
        # Обновление таблицы
        self.filtered_workouts = filtered if filter_applied else self.workouts
        self.refresh_table(self.filtered_workouts)
        
        # Обновление статуса
        if filter_applied:
            self.status_var.set(f"🔍 Найдено записей: {len(filtered)}")
        else:
            self.status_var.set("📋 Показаны все записи")
            
    def clear_filters(self):
        """Сброс всех фильтров"""
        self.filter_type_var.set("Все")
        self.filter_date_from_var.set("")
        self.filter_date_to_var.set("")
        
        self.refresh_table()
        self.update_statistics()
        self.status_var.set("🔄 Фильтры сброшены")
        
    def delete_selected_from_button(self):
        """Удаление выбранной записи"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ Предупреждение", "Выберите запись для удаления")
            return
            
        if messagebox.askyesno("❓ Подтверждение", "Вы уверены, что хотите удалить выбранную тренировку?"):
            for item in selected:
                values = self.tree.item(item)['values']
                # Поиск и удаление из основного списка
                for workout in self.workouts[:]:
                    if (workout['date'] == values[1] and 
                        workout['type'] == values[2] and 
                        workout['duration'] == int(values[3])):
                        self.workouts.remove(workout)
                        break
                        
            self.refresh_table()
            self.update_statistics()
            self.save_data()
            self.status_var.set("🗑️ Запись успешно удалена")
            
    def edit_selected(self):
        """Редактирование выбранной записи"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ Предупреждение", "Выберите запись для редактирования")
            return
            
        if len(selected) > 1:
            messagebox.showwarning("⚠️ Предупреждение", "Выберите только одну запись")
            return
            
        # Получение данных выбранной записи
        item = selected[0]
        values = self.tree.item(item)['values']
        
        # Создание окна редактирования
        edit_window = tk.Toplevel(self.root)
        edit_window.title("✏️ Редактирование тренировки")
        edit_window.geometry("400x250")
        edit_window.resizable(False, False)
        
        # Форма редактирования
        ttk.Label(edit_window, text="Дата (ДД.ММ.ГГГГ):").pack(pady=5)
        edit_date = ttk.Entry(edit_window, width=30)
        edit_date.insert(0, values[1])
        edit_date.pack(pady=5)
        
        ttk.Label(edit_window, text="Длительность (мин):").pack(pady=5)
        edit_duration = ttk.Entry(edit_window, width=30)
        edit_duration.insert(0, values[3])
        edit_duration.pack(pady=5)
        
        def save_changes():
            new_date = edit_date.get().strip()
            new_duration = edit_duration.get().strip()
            
            # Валидация
            date_valid, date_error = self.validate_date(new_date)
            if not date_valid:
                messagebox.showerror("❌ Ошибка", date_error)
                return
                
            duration_valid, duration_error = self.validate_duration(new_duration)
            if not duration_valid:
                messagebox.showerror("❌ Ошибка", duration_error)
                return
                
            # Обновление записи
            for workout in self.workouts:
                if (workout['date'] == values[1] and 
                    workout['type'] == values[2] and 
                    workout['duration'] == int(values[3])):
                    workout['date'] = new_date
                    workout['duration'] = int(new_duration)
                    workout['intensity'] = self.calculate_intensity(int(new_duration))
                    break
                    
            self.refresh_table()
            self.update_statistics()
            self.save_data()
            edit_window.destroy()
            self.status_var.set("✏️ Запись успешно отредактирована")
            
        tk.Button(
            edit_window,
            text="💾 Сохранить изменения",
            command=save_changes,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 10),
            padx=20,
            pady=5
        ).pack(pady=10)
        
    def clear_all(self):
        """Очистка всех записей"""
        if not self.workouts:
            messagebox.showinfo("ℹ️ Информация", "Нет записей для удаления")
            return
            
        if messagebox.askyesno("⚠️ Подтверждение", 
                              f"Вы уверены, что хотите удалить ВСЕ {len(self.workouts)} записей?\n\nЭто действие нельзя отменить!"):
            self.workouts.clear()
            self.refresh_table()
            self.update_statistics()
            self.save_data()
            self.status_var.set("🗑️ Все записи удалены")
            
    def clear_input_fields(self):
        """Очистка полей ввода"""
        self.date_var.set(datetime.now().strftime('%d.%m.%Y'))
        self.type_var.set("Выберите тип")
        self.duration_var.set("")
        self.date_entry.focus()
        
    def on_double_click(self, event):
        """Обработка двойного клика по таблице"""
        self.edit_selected()
        
    def update_statistics(self):
        """Обновление статистической информации"""
        if not self.workouts:
            self.stats_text.set("📊 Статистика: Нет данных")
            return
            
        total_workouts = len(self.workouts)
        total_duration = sum(w['duration'] for w in self.workouts)
        avg_duration = total_duration / total_workouts
        min_duration = min(w['duration'] for w in self.workouts)
        max_duration = max(w['duration'] for w in self.workouts)
        
        # Подсчет по типам
        types_count = {}
        for w in self.workouts:
            types_count[w['type']] = types_count.get(w['type'], 0) + 1
        most_common = max(types_count, key=types_count.get)
        
        stats = (
            f"📊 Всего тренировок: {total_workouts} | "
            f"Общее время: {total_duration} мин ({total_duration//60} ч {total_duration%60} мин) | "
            f"Средняя: {avg_duration:.1f} мин | "
            f"Мин: {min_duration} мин | "
            f"Макс: {max_duration} мин | "
            f"Любимый тип: {most_common} ({types_count[most_common]})"
        )
        
        self.stats_text.set(stats)
        
    # Методы работы с файлами
    def save_data(self, show_message=False):
        """Сохранение данных в JSON файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump({
                    'workouts': self.workouts,
                    'saved_at': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
                    'total_workouts': len(self.workouts)
                }, file, ensure_ascii=False, indent=4)
                
            if show_message:
                self.status_var.set(f"💾 Данные сохранены в {self.data_file}")
                messagebox.showinfo("✅ Успех", f"Данные сохранены в файл:\n{self.data_file}")
        except Exception as e:
            messagebox.showerror("❌ Ошибка сохранения", f"Не удалось сохранить файл:\n{str(e)}")
            
    def load_data(self):
        """Загрузка данных из JSON файла"""
        if not os.path.exists(self.data_file):
            self.status_var.set("ℹ️ Файл данных не найден. Создайте новую тренировку.")
            return
            
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.workouts = data.get('workouts', [])
                
            self.refresh_table()
            self.update_statistics()
            saved_at = data.get('saved_at', 'неизвестно')
            self.status_var.set(f"📂 Данные загружены. Последнее сохранение: {saved_at}")
            
        except json.JSONDecodeError:
            messagebox.showerror("❌ Ошибка", "Файл данных поврежден. Будет создан новый.")
            self.workouts = []
            self.refresh_table()
        except Exception as e:
            messagebox.showerror("❌ Ошибка загрузки", f"Не удалось загрузить файл:\n{str(e)}")
            
    def export_data(self):
        """Экспорт данных в новый JSON файл"""
        if not self.workouts:
            messagebox.showwarning("⚠️ Предупреждение", "Нет данных для экспорта")
            return
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_file = f"workouts_export_{timestamp}.json"
        
        try:
            with open(export_file, 'w', encoding='utf-8') as file:
                json.dump({
                    'workouts': self.workouts,
                    'exported_at': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
                    'total_workouts': len(self.workouts),
                    'statistics': {
                        'total_duration': sum(w['duration'] for w in self.workouts),
                        'avg_duration': sum(w['duration'] for w in self.workouts) / len(self.workouts),
                        'workout_types': list(set(w['type'] for w in self.workouts))
                    }
                }, file, ensure_ascii=False, indent=4)
                
            self.status_var.set(f"📤 Данные экспортированы в {export_file}")
            messagebox.showinfo("✅ Экспорт", f"Данные успешно экспортированы в файл:\n{export_file}")
            
        except Exception as e:
            messagebox.showerror("❌ Ошибка экспорта", f"Не удалось экспортировать данные:\n{str(e)}")
            
    # Вспомогательные методы
    def show_about(self):
        """Показать информацию о программе"""
        about_window = tk.Toplevel(self.root)
        about_window.title("О программе")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        info = """
🏋️ TRAINING PLANNER v1.0
        
Планировщик тренировок с графическим 
интерфейсом для отслеживания ваших 
спортивных достижений.

Возможности:
• Добавление тренировок
• Фильтрация по типу и дате
• Сохранение в JSON
• Статистика тренировок
• Экспорт данных

Язык: Python 3.x
Интерфейс: Tkinter
        """
        
        tk.Label(about_window, text=info, font=('Arial', 10), justify=tk.LEFT).pack(pady=20)
        tk.Button(
            about_window,
            text="OK",
            command=about_window.destroy,
            width=15,
            bg=self.colors['primary'],
            fg='white'
        ).pack(pady=10)
        
    def show_help(self):
        """Показать справку"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Справка")
        help_window.geometry("500x400")
        help_window.resizable(True, True)
        
        help_text = """
📚 СПРАВКА ПО ИСПОЛЬЗОВАНИЮ

1. ДОБАВЛЕНИЕ ТРЕНИРОВКИ:
   • Введите дату в формате ДД.ММ.ГГГГ
   • Выберите тип тренировки из списка
   • Укажите длительность в минутах
   • Нажмите "ДОБАВИТЬ ТРЕНИРОВКУ"

2. ФИЛЬТРАЦИЯ:
   • Выберите тип или диапазон дат
   • Нажмите "Применить"
   • Для сброса нажмите "Сбросить"

3. РЕДАКТИРОВАНИЕ:
   • Двойной клик по записи
   • Или правый клик → Редактировать

4. УДАЛЕНИЕ:
   • Выберите запись и нажмите Delete
   • Или используйте контекстное меню

5. СОХРАНЕНИЕ:
   • Автоматическое после каждого действия
   • Ручное через меню Файл → Сохранить

6. ЭКСПОРТ:
   • Меню Файл → Экспорт в JSON
   • Создает файл с временной меткой

ГОРЯЧИЕ КЛАВИШИ:
   Ctrl+S - Сохранить
   Ctrl+L - Загрузить
   Ctrl+Q - Выйти
   Delete - Удалить запись
        """
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, font=('Arial', 10))
        text_widget.insert('1.0', help_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Button(
            help_window,
            text="Закрыть",
            command=help_window.destroy,
            width=15,
            bg=self.colors['primary'],
            fg='white'
        ).pack(pady=10)

def main():
    """Главная функция запуска приложения"""
    try:
        root = tk.Tk()
        app = TrainingPlanner(root)
        root.mainloop()
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        messagebox.showerror("Критическая ошибка", f"Приложение завершило работу с ошибкой:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
