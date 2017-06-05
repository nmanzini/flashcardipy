import tkinter as tk

import sqlite3

from main import Word, chooser

name = 'test01.db'
filename = "grelist.txt"
conn = sqlite3.connect(name)
c = conn.cursor()

class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        test_word = Word(chooser())
        word = test_word.word
        definition = test_word.definition

        self.word_lbl = tk.Label(text=word)
        self.question = tk.Label(text="you know dis?")
        self.yes_btn = tk.Button(text="yes", width=12)
        self.no_btn = tk.Button(text="no", width=12)
        self.definition_lbl = tk.Label(text=definition, wraplength=200)
        self.continue_btn = tk.Button(text="continue", command=self.get_new_word, width=12)

        self.word_lbl.grid(row=0, columnspan=2, sticky="nsew")
        self.question.grid(row=1, columnspan=2)
        self.yes_btn.grid(row=2, column=0, padx=5)
        self.no_btn.grid(row=2, column=1, padx=5)
        self.definition_lbl.grid(row=3, columnspan=2)
        self.continue_btn.grid(row=4, columnspan=2)

    def get_new_word(self):
        test_word = Word(chooser())
        print("changing word")
        print(test_word.word, test_word.definition)
        self.word_lbl["text"] = test_word.word
        self.definition_lbl["text"] = test_word.definition
        print()

c.close()
conn.close()

root = tk.Tk()
root.geometry("220x180")
app = App(root)
app.mainloop()

