# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog
import json
import nltk
from nltk.corpus import wordnet as wn
import random
import time

# Загрузка WordNet
nltk.download('wordnet')

# Список сайтов и соответствующих им конфигураций
websites = {
    "Site 1": {
        "url": None,
        "config_file": None,
        "parse_function": None
    },
    "Site 2": {
        "url": None,
        "config_file": None,
        "parse_function": None
    },
    "Site 3": {
        "url": None,
        "config_file": None,
        "parse_function": None
    }
}

# Загрузка конфигурации для каждого сайта
site_configs = {}


def load_config_file(site):
    file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, "r") as file:
            site_configs[site] = json.load(file)


def open_config_file(site):
    load_config_file(site)


def create_site_fields():
    row = 150
    for site in websites:
        label = tk.Label(frame, text=site, font=("Helvetica", 12), foreground="white")
        label.place(x=50, y=row)

        url_entry = tk.Entry(frame, font=("Helvetica", 12))
        url_entry.place(x=200, y=row)

        config_entry = tk.Entry(frame, font=("Helvetica", 12))
        config_entry.place(x=400, y=row, width=250)

        browse_button = ttk.Button(frame, text="Обзор", command=lambda s=site: open_config_file(s))
        browse_button.place(x=660, y=row)

        parse_checkbutton = ttk.Checkbutton(frame, text="Парсинг", variable=websites[site]["parse_function"])
        parse_checkbutton.place(x=740, y=row)

        websites[site]["url"] = url_entry
        websites[site]["config_file_entry"] = config_entry

        row += 30


def create_json():
    start_line = int(start_entry.get())
    end_line = int(end_entry.get())

    with open("236k-of-words.txt", "r") as file:
        lines = file.readlines()[start_line - 1:end_line]
        words = [line.strip() for line in lines]

    data = []

    for word in words:
        word_data = {"word": word}

        for site, config in site_configs.items():
            url = websites[site]["url"].get()
            parse_function = websites[site]["parse_function"].get()
            if parse_function:
                parsed_data = parse_function(url, config)
                word_data.update(parsed_data)

            # Задержка перед каждым запросом
            if use_delay.get():
                delay = random.uniform(0.5, 2.0)
                time.sleep(delay)

        data.append(word_data)

    json_data = json.dumps(data, indent=4)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, json_data)


def export_json():
    json_data = output_text.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(json_data)


def select_all(event):
    output_text.tag_add("sel", "1.0", "end")
    return "break"


def parse_site1(url, config):
    # Реализация парсинга для Site 1
    translations = ["Translation 1", "Translation 2"]
    examples = ["Example 1", "Example 2"]

    # Возвращаем случайно выбранные элементы из списков
    translation = random.choice(translations)
    example = random.choice(examples)

    return {
        "translations": translation,
        "examples": example
    }


def parse_site2(url, config):
    # Реализация парсинга для Site 2
    translations = ["Translation 1", "Translation 2"]
    transcription = "Transcription"

    # Возвращаем случайно выбранный элемент из списка
    translation = random.choice(translations)

    return {
        "translations": translation,
        "transcription": transcription
    }


def parse_site3(url, config):
    # Реализация парсинга для Site 3
    usage_examples = ["Usage Example 1", "Usage Example 2"]

    # Возвращаем случайно выбранный элемент из списка
    usage_example = random.choice(usage_examples)

    return {
        "usage_examples": usage_example
    }


def toggle_parse_function(site):
    parse_function = websites[site]["parse_function"]
    if parse_function.get():
        parse_function.set(None)
    else:
        parse_function.set(parse_site1)


def toggle_proxy():
    if use_proxy.get():
        # Включить использование прокси
        pass
    else:
        # Отключить использование прокси
        pass


def toggle_delay():
    if use_delay.get():
        # Включить использование задержки
        pass
    else:
        # Отключить использование задержки
        pass


# Создание главного окна
window = tk.Tk()
window.title("English-russian dictionary JSON Combine")
window.iconphoto(True, tk.PhotoImage(file="icon.png"))

# Создание фрейма с фоновым изображением
frame = tk.Frame(window)
frame.pack(fill="both", expand=True)

background_image = tk.PhotoImage(file="background.png")
background_label = tk.Label(frame, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Настройка стиля для кнопок
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), foreground="white", background="#007bff")

# Настройка меток и полей ввода
start_label = tk.Label(frame, text="Старт со слова ( число от 1 ):", font=("Helvetica", 14), foreground="white")
start_label.place(x=50, y=50)
start_entry = tk.Entry(frame, font=("Helvetica", 12))
start_entry.place(x=400, y=50)

end_label = tk.Label(frame, text="Заканчиваем на слове ( число до 236736 ):", font=("Helvetica", 14), foreground="white")
end_label.place(x=50, y=100)
end_entry = tk.Entry(frame, font=("Helvetica", 12))
end_entry.place(x=400, y=100)

# Создание полей и кнопок для настроек каждого сайта
create_site_fields()

# Настройка кнопки для создания JSON
create_button = ttk.Button(frame, text="Создать JSON'ы", command=create_json)
create_button.place(x=200, y=450)

# Настройка кнопки для экспорта JSON
export_button = ttk.Button(frame, text="Экспорт JSON", command=export_json)
export_button.place(x=350, y=450)

# Настройка текстового поля для вывода JSON
output_text = tk.Text(frame, font=("Helvetica", 12), height=10)
output_text.place(x=50, y=500, width=700)
output_text.bind("<Command-a>", select_all)

# Настройка чекбоксов для включения/отключения парсинга, использования прокси и задержки
row = 150
for site in websites:
    parse_checkbutton = ttk.Checkbutton(frame, text="Парсинг", variable=websites[site]["parse_function"])
    parse_checkbutton.place(x=740, y=row)
    row += 30

use_proxy = tk.BooleanVar()
proxy_checkbutton = ttk.Checkbutton(frame, text="Использовать прокси", variable=use_proxy)
proxy_checkbutton.place(x=700, y=50)

use_delay = tk.BooleanVar()
delay_checkbutton = ttk.Checkbutton(frame, text="Использовать задержку", variable=use_delay)
delay_checkbutton.place(x=700, y=100)

# Запуск главного цикла приложения
window.geometry("800x600")
window.mainloop()
