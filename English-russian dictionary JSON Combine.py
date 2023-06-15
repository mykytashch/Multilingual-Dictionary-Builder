import tkinter as tk
from tkinter import ttk, filedialog
import json
from parsing_config_site1 import parse_site1
from parsing_config_site2 import parse_site2
from parsing_config_site3 import parse_site3
from synonyms_and_similar_words import create_synonyms_and_similar_words
from threading import Thread
import time


def create_json():
    start_line = int(start_entry.get())
    end_line = int(end_entry.get())

    with open("236k-of-words.txt", "r") as file:
        lines = file.readlines()[start_line - 1:end_line]
        words = [line.strip() for line in lines]

    data = []

    for word in words:
        word_data = {"word": word}

        if parse_site1.get():
            parsed_data_site1 = parse_site1(word)
            word_data.update(parsed_data_site1)

        if parse_site2.get():
            parsed_data_site2 = parse_site2(word)
            word_data.update(parsed_data_site2)

        if parse_site3.get():
            parsed_data_site3 = parse_site3(word)
            word_data.update(parsed_data_site3)

        if use_synonyms.get():
            synonyms_and_similar_words = create_synonyms_and_similar_words(word)
            word_data.update(synonyms_and_similar_words)

        output_text.insert(tk.END, json.dumps(word_data, indent=4))
        output_text.insert(tk.END, '\n')

        output_text.see(tk.END)  # Прокрутить до конца текстового поля

        if use_delay.get():
            delay = float(delay_combobox.get().replace("с", ""))
            time.sleep(delay)


def export_json():
    json_data = output_text.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(json_data)


def toggle_proxy():
    proxy_button["state"] = "normal" if use_proxy.get() else "disabled"
    delay_combobox["state"] = "readonly" if use_delay.get() else "disabled"


def load_proxy_list():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        proxy_list = read_proxy_list(file_path)
        # Загрузить список прокси в функции парсинга


def read_proxy_list(file_path):
    with open(file_path, "r") as file:
        proxy_list = [line.strip() for line in file.readlines()]
    return proxy_list


def parse_words(words):
    for word in words:
        word_data = {"word": word}

        if parse_site1.get():
            parsed_data_site1 = parse_site1(word)
            word_data.update(parsed_data_site1)

        if parse_site2.get():
            parsed_data_site2 = parse_site2(word)
            word_data.update(parsed_data_site2)

        if parse_site3.get():
            parsed_data_site3 = parse_site3(word)
            word_data.update(parsed_data_site3)

        if use_synonyms.get():
            synonyms_and_similar_words = create_synonyms_and_similar_words(word)
            word_data.update(synonyms_and_similar_words)

        output_text.insert(tk.END, json.dumps(word_data, indent=4))
        output_text.insert(tk.END, '\n')

        output_text.see(tk.END)  # Прокрутить до конца текстового поля

        if use_delay.get():
            delay = float(delay_combobox.get().replace("с", ""))
            time.sleep(delay)


def create_json_async():
    start_line = int(start_entry.get())
    end_line = int(end_entry.get())

    with open("236k-of-words.txt", "r") as file:
        lines = file.readlines()[start_line - 1:end_line]
        words = [line.strip() for line in lines]

    output_text.delete("1.0", tk.END)

    thread = Thread(target=parse_words, args=(words,))
    thread.start()


window = tk.Tk()
window.title("English-Russian Dictionary")
window.geometry("800x600")

# Установка иконки приложения
window.iconphoto(True, tk.PhotoImage(file="icon.png"))

frame = ttk.Frame(window)
frame.pack(fill="both", expand=True)

# Установка фонового изображения
background_image = tk.PhotoImage(file="background.png")
background_label = tk.Label(frame, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

start_label = tk.Label(frame, text="Старт со слова ( число от 1 ):", font=("Helvetica", 14), foreground="white")
start_label.grid(row=0, column=0, padx=10, pady=5)
start_entry = tk.Entry(frame, font=("Helvetica", 12))
start_entry.grid(row=0, column=1, padx=10, pady=5)

end_label = tk.Label(frame, text="Заканчиваем на слове ( число до 236736 ):", font=("Helvetica", 14), foreground="white")
end_label.grid(row=0, column=2, padx=10, pady=5)
end_entry = tk.Entry(frame, font=("Helvetica", 12))
end_entry.grid(row=0, column=3, padx=10, pady=5)

parse_site1 = tk.BooleanVar()
parse_site2 = tk.BooleanVar()
parse_site3 = tk.BooleanVar()
use_synonyms = tk.BooleanVar()

parse_site1_checkbutton = ttk.Checkbutton(frame, text="Парсинг с сайта 1", variable=parse_site1)
parse_site1_checkbutton.grid(row=1, column=0, padx=10, pady=5, columnspan=2)

parse_site2_checkbutton = ttk.Checkbutton(frame, text="Парсинг с сайта 2", variable=parse_site2)
parse_site2_checkbutton.grid(row=1, column=2, padx=10, pady=5, columnspan=2)

parse_site3_checkbutton = ttk.Checkbutton(frame, text="Парсинг с сайта 3", variable=parse_site3)
parse_site3_checkbutton.grid(row=2, column=0, padx=10, pady=5, columnspan=2)

use_synonyms_checkbutton = ttk.Checkbutton(frame, text="Использовать синонимы и похожие слова", variable=use_synonyms)
use_synonyms_checkbutton.grid(row=2, column=2, padx=10, pady=5, columnspan=2)

use_proxy = tk.BooleanVar()
proxy_checkbutton = ttk.Checkbutton(frame, text="Использовать прокси", variable=use_proxy, command=toggle_proxy)
proxy_checkbutton.grid(row=3, column=0, padx=10, pady=5, columnspan=2)

proxy_button = ttk.Button(frame, text="Загрузить прокси", state="disabled", command=load_proxy_list)
proxy_button.grid(row=3, column=2, padx=10, pady=5, columnspan=2)

use_delay = tk.BooleanVar()
delay_checkbutton = ttk.Checkbutton(frame, text="Использовать задержку", variable=use_delay, command=toggle_proxy)
delay_checkbutton.grid(row=4, column=0, padx=10, pady=5, columnspan=2)

delay_combobox = ttk.Combobox(frame, state="readonly", width=5)
delay_combobox.grid(row=4, column=2, padx=10, pady=5, columnspan=2)
delay_values = [str(i / 10) + "с" for i in range(1, 151)]
delay_combobox["values"] = delay_values

create_button = ttk.Button(frame, text="Создать JSON'ы", command=create_json_async)
create_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

export_button = ttk.Button(frame, text="Экспорт JSON", command=export_json)
export_button.grid(row=5, column=2, columnspan=2, padx=10, pady=10)

output_text = tk.Text(frame, font=("Helvetica", 12), height=10, width=80)
output_text.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

window.mainloop()
