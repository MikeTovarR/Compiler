import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from File_Handler import FileHandler
from Lexer import Lexer

class TokenGUI:
    def __init__(self, root, file_location):
        self.file_location = file_location

        self.root = root
        self.root.title("Token Analyzer")

        self.label_variables = tk.Label(root, text="Variables and Tokens:")
        self.label_variables.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.treeview = ttk.Treeview(root, columns=("Word", "Token"), show="headings")
        self.treeview.heading("Word", text="Word")
        self.treeview.heading("Token", text="Token")
        self.treeview.grid(row=1, column=0, padx=5, pady=5)

        self.button_analyze = tk.Button(root, text="Analyze", command=self.analyze_file)
        self.button_analyze.grid(row=2, column=0, padx=5, pady=5)

    def analyze_file(self):
        file_handler = FileHandler(self.file_location)
        text = file_handler.read_file()
        if text is not None:
            lexer = Lexer(text)
            lexer.run()
            tokens = lexer.get_tokens()
            self.display_tokens(tokens)
        else:
            messagebox.showerror("File Not Found", f"File {file_location} not found.")

    def display_tokens(self, tokens):
        for token in tokens:
            self.treeview.insert("", "end", values=(token.get_word(), token.get_token()))