import tkinter as tk
from tkinter import messagebox
import math
import winsound  # Для звуковых эффектов
import customtkinter as ctk
from VibeButtons import RoundedButton
# --- КОНФИГУРАЦИЯ ТЕМ ---
THEMES = {
    "dark": {
        "bg": "#121212", "display_bg": "#1E1E1E", "text": "#FFFFFF",
        "btn_num": "#2C2C2C", "btn_op": "#A8A8A8", "btn_fn": "#A5A5A5", "btn_eq": "#4CAF50"
    },
    "ocean": {
        "bg": "#0D1B2A", "display_bg": "#1B263B", "text": "#E0E1DD",
        "btn_num": "#415A77", "btn_op": "#778DA9", "btn_fn": "#1B263B", "btn_eq": "#00B4D8"
    }
}

class ModernButton(tk.Button):
    def __init__(self, master, text, bg, fg, command, **kwargs):
        super().__init__(master, text=text, command=command, font=("Segoe UI", 12, "bold"),
                         bg=bg, fg=fg, bd=0, relief="flat", activebackground="#555555",
                         highlightthickness=3)
        self.default_bg = bg
        self.bind("<Enter>", lambda e: self.config(bg="#666666"))
        self.bind("<Leave>", lambda e: self.config(bg=self.default_bg))
        # Звук при нажатии
        self.bind("<Button-1>", lambda e: winsound.Beep(600, 20)) 

class App(ctk.CTk): # Основной класс приложения
    def __init__(self):
        super().__init__()
        self.title("VibeCalc Pro + Audio")# Название окна
        self.geometry("400x650")
        
        self.current_theme = "dark"
        self.is_scientific = False
        self.history = [] # Список для хранения истории
        self.history_visible = False
        self.display_var = tk.StringVar(value="0")
        
        self.setup_ui()
        self.apply_theme("dark")
    
    def play_sound(self, type):
        if type == "click":
            winsound.Beep(800, 30) # Высокий короткий писк
        elif type == "equal":
            winsound.Beep(1000, 50) # Звук результата
        elif type == "error":
            winsound.MessageBeep() # Системный звук ошибки

    def setup_ui(self):# Инициализация интерфейса
        # Основное Меню
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        
        mode_menu = tk.Menu(self.menubar, tearoff=0)
        mode_menu.add_command(label="Обычный", command=self.set_standard)
        mode_menu.add_command(label="Инженерный", command=self.set_scientific)
        # В раздел, где создаешь mode_menu
        mode_menu.add_command(label="Сохранить историю", command=self.save_history)
        self.menubar.add_cascade(label="Режим", menu=mode_menu)

        # Верхняя панель (Дисплей + Кнопка истории)
        self.top_panel = tk.Frame(self)
        self.top_panel.pack(fill="x", padx=10, pady=10)
        
        self.btn_hist = tk.Button(self.top_panel, text="📜 История", command=self.toggle_history, 
                                  bd=0, bg="#333", fg="white", font=("Arial", 9))
        self.btn_hist.pack(side="top", anchor="e")

        self.display_label = tk.Label(self.top_panel, textvariable=self.display_var, 
                                      font=("Segoe UI", 36), anchor="e", padx=10)
        self.display_label.pack(fill="x")

        # Основной контейнер для кнопок и истории
        self.main_container = tk.Frame(self)
        self.main_container.pack(fill="both", expand=True)

        self.btns_container = tk.Frame(self.main_container)
        self.btns_container.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Боковая панель истории (скрыта по умолчанию)
        self.history_frame = tk.Frame(self.main_container, width=0)
        self.history_list = tk.Listbox(self.history_frame, font=("Arial", 10), bd=0)
        self.history_list.pack(fill="both", expand=True)

        self.render_buttons()

    def render_buttons(self):# Отрисовка кнопок
        # Сначала очищаем контейнер кнопок
        for widget in self.btns_container.winfo_children():
            widget.destroy()

        if self.is_scientific:
            layout = [
                ('sin', 0, 0, 'op'), ('cos', 0, 1, 'op'), ('tan', 0, 2, 'op'), ('log', 0, 3, 'op'),
                ('√', 1, 0, 'op'), ('^', 1, 1, 'op'), ('π', 1, 2, 'op'), ('C', 1, 3, 'fn'),
                ('7', 2, 0, 'num'), ('8', 2, 1, 'num'), ('9', 2, 2, 'num'), ('/', 2, 3, 'op'),
                ('4', 3, 0, 'num'), ('5', 3, 1, 'num'), ('6', 3, 2, 'num'), ('*', 3, 3, 'op'),
                ('1', 4, 0, 'num'), ('2', 4, 1, 'num'), ('3', 4, 2, 'num'), ('-', 4, 3, 'op'),
                ('0', 5, 0, 'num'), ('.', 5, 1, 'num'), ('=', 5, 2, 'eq', 2)
            ]
            cols = 4
        else:
            layout = [
                ('C', 0, 0, 'fn'), ('⌫', 0, 1, 'fn'), ('%', 0, 2, 'fn'), ('/', 0, 3, 'op'),
                ('7', 1, 0, 'num'), ('8', 1, 1, 'num'), ('9', 1, 2, 'num'), ('*', 1, 3, 'op'),
                ('4', 2, 0, 'num'), ('5', 2, 1, 'num'), ('6', 2, 2, 'num'), ('-', 2, 3, 'op'),
                ('1', 3, 0, 'num'), ('2', 3, 1, 'num'), ('3', 3, 2, 'num'), ('+', 3, 3, 'op'),
                ('0', 4, 0, 'num', 2), ('.', 4, 2, 'num'), ('=', 4, 3, 'eq')
            ]
            cols = 4

        for r in range(6): self.btns_container.grid_rowconfigure(r, weight=1)
        for c in range(cols): self.btns_container.grid_columnconfigure(c, weight=1)

        theme = THEMES[self.current_theme]
        for item in layout:
            text, r, c, btype = item[0], item[1], item[2], item[3]
            cspan = item[4] if len(item) > 4 else 1
            
            if btype == 'num': bg, fg = theme['btn_num'], theme['text']
            elif btype == 'op': bg, fg = theme['btn_op'], "white"
            elif btype == 'eq': bg, fg = theme['btn_eq'], "white"
            else: bg, fg = theme['btn_fn'], "black"

            # Создаем кнопку с заданными параметрами:
            btn = RoundedButton(self.btns_container, 
                    text=text, 
                    btype=btype, 
                    command=lambda t=text: self.handle_click(t))
            btn.grid(row=r, column=c, columnspan=cspan, sticky="nsew", padx=5, pady=5)

    def handle_click(self, char):# Обработка нажатий кнопок
        curr = self.display_var.get()
        
        if char == 'C': 
            self.display_var.set("0")
        elif char == '⌫':
            self.display_var.set(curr[:-1] if len(curr)>1 else "0")
        elif char == '√':
            try:
                # Берем число из дисплея, превращаем в float и считаем корень
                val = float(curr)
                if val < 0: raise ValueError("Negative")
                res = math.sqrt(val)
                self.display_var.set(str(round(res, 6)))
                self.history.append(f"√({val}) = {res}")
                self.update_history_list()
            except:
                winsound.MessageBeep() 
                self.display_var.set("Error")
        elif char == '=':
            try:
                # Заменяем ^ на ** для Python, чтобы работало возведение в степень
                temp_expr = curr.replace('^', '**').replace('π', str(math.pi))
                res = str(eval(temp_expr))
                self.history.append(f"{curr} = {res}")
                self.update_history_list()
                self.display_var.set(res[:14])
            except:
                winsound.MessageBeep()
                self.display_var.set("Error")
        else:
            self.display_var.set(char if curr == "0" else curr + char)

    def toggle_history(self):# Переключение видимости истории
        if not self.history_visible:
            self.history_frame.pack(side="right", fill="y", padx=5)
            self.geometry("600x650") # Расширяем окно для истории
        else:
            self.history_frame.pack_forget()
            self.geometry("400x650")
        self.history_visible = not self.history_visible

    def update_history_list(self):# Обновление списка истории
        self.history_list.delete(0, tk.END)
        for item in reversed(self.history):
            self.history_list.insert(tk.END, item)
            
    def save_history(self):# Сохранение истории в файл
        try:
            with open("calculator_history.txt", "w", encoding="utf-8") as file:
                for item in self.history:
                    file.write(item + "\n")
            messagebox.showinfo("Успех", "История сохранена в файл calculator_history.txt")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    def apply_theme(self, theme_name):# Применение темы
        theme = THEMES[theme_name]
        self.configure(bg=theme['bg'])
        self.top_panel.configure(bg=theme['bg'])
        self.display_label.configure(bg=theme['display_bg'], fg=theme['text'])
        self.history_frame.configure(bg=theme['display_bg'])
        self.history_list.configure(bg=theme['display_bg'], fg=theme['text'])
        self.render_buttons()

    def set_standard(self):# Переключение на стандартный режим
        self.is_scientific = False
        self.render_buttons()

    def set_scientific(self):# Переключение на инженерный режим
        self.is_scientific = True
        self.render_buttons()

if __name__ == "__main__":
    app = App()
    app.mainloop()