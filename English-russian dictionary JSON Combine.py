import tkinter as tk
from tkinter import ttk, filedialog
import json
from nltk.corpus import wordnet as wn

def create_json():
    start_line = int(start_entry.get())
    end_line = int(end_entry.get())

    with open("236k-of-words.txt", "r") as file:
        lines = file.readlines()[start_line-1:end_line]
        words = [line.strip() for line in lines]

    data = []

    for word in words:
        # Получаем транскрипцию, если флажок включен
        transcription = get_transcription(word) if transcription_var.get() else None

        # Получаем переводы и примеры использования, если флажок включен
        translations, examples = get_translations_and_examples(word) if translations_var.get() else (None, None)

        # Получаем похожие слова и синонимы, если флажок включен
        similar_words = get_similar_words(word) if similar_words_var.get() else None

        word_data = {
            "word": word,
            "transcription": transcription,
            "translations": translations,
            "examples": examples,
            "similar_words": similar_words
        }

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

# Флажки для функций
transcription_var = tk.BooleanVar()
transcription_checkbox = ttk.Checkbutton(frame, text="Транскрипция", variable=transcription_var)
transcription_checkbox.place(x=50, y=150)

translations_var = tk.BooleanVar()
translations_checkbox = ttk.Checkbutton(frame, text="Переводы и примеры использования", variable=translations_var)
translations_checkbox.place(x=50, y=180)

similar_words_var = tk.BooleanVar()
similar_words_checkbox = ttk.Checkbutton(frame, text="Похожие слова и синонимы", variable=similar_words_var)
similar_words_checkbox.place(x=50, y=210)

# Настройка кнопки для создания JSON
create_button = ttk.Button(frame, text="Создать JSON'ы", command=create_json)
create_button.place(x=200, y=250)

# Настройка кнопки для экспорта JSON
export_button = ttk.Button(frame, text="Экспорт JSON", command=export_json)
export_button.place(x=350, y=250)

# Настройка текстового поля для вывода JSON
output_text = tk.Text(frame, font=("Helvetica", 12), height=10)
output_text.place(x=50, y=300, width=500)
output_text.bind("<Command-a>", select_all)

# Запуск главного цикла приложения
window.geometry("600x550")
window.mainloop()
