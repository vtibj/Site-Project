import customtkinter as ctk

# Настройка внешнего вида по умолчанию
ctk.set_appearance_mode("dark")  # Тема: "dark" или "light"
ctk.set_default_color_theme("blue") # Цвета: "blue", "green", "dark-blue"

class RoundedButton(ctk.CTkButton):
    def __init__(self, master, text, command, btype="num", **kwargs):
        # Определяем цвета в зависимости от типа кнопки
        if btype == "num":
            fg_color = "#333333"      # Темно-серый для цифр
            hover_color = "#444444"
            text_color = "white"
        elif btype == "op":
            fg_color = "#A8A8A8"      # Оранжевый для операций
            hover_color = "#A8A8A8"
            text_color = "white"
        elif btype == "eq":
            fg_color = "#4CAF50"      # Зеленый для равно
            hover_color = "#66BB6A"
            text_color = "white"
        else: # btype == "fn"
            fg_color = "#A5A5A5"      # Светло-серый для функций
            hover_color = "#D4D4D4"
            text_color = "black"

        super().__init__(master, 
                         text=text, 
                         command=command,
                         corner_radius=20,    # ВОТ ОНО! Радиус скругления
                         fg_color=fg_color,
                         hover_color=hover_color,
                         text_color=text_color,
                         font=("Segoe UI", 16, "bold"),
                         height=50,           # Высота кнопки
                         **kwargs)