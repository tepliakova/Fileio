from http.client import responses
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk
import requests
import pyperclip
import json
import os

history_file = 'upload_history.json'


def save_history(file_path, link):
    history = []
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    history.uppend({"file_path": os.path.basename(file_path), "download_link": link})
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4)



def upload():
    try:
        filepath = fd.askopenfilename()
        if filepath:
            with open (filepath, 'rb') as f:
                files = {'file': f}
                response = requests.post('https://file.io', files = files)
                response.raise_for_status()
                link = response.json()['link']
                entry.delete(0, END)
                entry.insert(0, link)
                save_history(filepath, link)
                pyperclip.copy(link)
                mb.showinfo("Ссылка скопирована", f"Ссылка {link} успешно скопирована в буфер обмена")
    except Exception as e:
        mb.showerror("Ошибка", f"Произошла ошибка: {e}")


window = Tk()
window.title("Сохранение файла в облаке")
window.geometry("400x200")

button = ttk.Button(text="Загрузить файл", command=upload)
button.pack()

entry = ttk.Entry()
entry.pack()

window.mainloop()