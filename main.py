import tkinter as tk
from tkinter import ttk
import customtkinter
from langdetect import detect
from googletrans import Translator
from googletrans import LANGUAGES
import time

translator = Translator()
texto = 'Olá eu sou théo e tenho 19 anos, jogo alguns jogos de vez enquando'
texto_traduzido = translator.translate(texto, src='pt', dest='en').text
print(texto_traduzido)

def show_search_button(event=None):
    if search_text.get("1.0", "end-1c").strip():
        search_button.grid(row=2, column=0, padx=10, pady=10)
    else:
        search_button.grid_forget()

# Bringing the languages
def searchLanguage():
    global detected_language
    global text
    text = search_text.get("1.0", "end-1c")

    if text.strip():
        try:
            detected_language = detect(text)
            result_label.config(text=f'O idioma detectado foi: {detected_language}')
            window.update()
            time.sleep(3)
            result_label.config(text=f'Você deseja traduzir seu texto para qual linguagem?')
            combo.grid(row=6, column=0, padx=10, pady=10)
        except:
            result_label.config(text=f'Erro ao detectar o idioma')


def translate():
    indice_selecionado = combo.current()
    opcao_selecionada = combo["values"][indice_selecionado]

    codigo_idioma = LANGUAGES.get(opcao_selecionada.capitalize())
    if codigo_idioma is None:
        print("Código de idioma não encontrado para:", opcao_selecionada)
        return

    translator = Translator()
    translated_text = translator.translate(search_text.get("1.0", tk.END), src=detected_language, dest=codigo_idioma)
    
    if translated_text is None:
        print("Falha na tradução:", opcao_selecionada)
        return

    search_text.delete("1.0", tk.END)  # Clear the current text
    search_text.insert(tk.END, translated_text.text)
    print("Texto traduzido:", translated_text.text)


window = tk.Tk()  # Creating a window for the code
window.geometry("400x240")
window.configure(bg="black")

search_text = tk.Text(window, height=5, width=30,)  # Adjust the size of the Text widget
search_text.grid(row=0, column=0, padx=10, pady=10)  # Adjust padding

search_button = tk.Button(window, text="Buscar Idioma", command=searchLanguage)
search_button.grid(row=3, column=0)
search_text.bind('<KeyRelease>', show_search_button)  # Bind to key release event

result_label = tk.Label(window, text="", fg="white", bg="black")  # Set label colors
result_label.grid(row=4, column=0)

select_language = tk.StringVar()
combo = ttk.Combobox(window, textvariable=select_language, values=[
    f"{language} - {LANGUAGES[language]}"
    for language in LANGUAGES
])

last_button = tk.Button(window, text="Check", command=translate)
last_button.grid(row=6, column=0)

window.mainloop()