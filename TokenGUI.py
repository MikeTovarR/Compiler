import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from File_Handler import FileHandler
from Lexer import Lexer
from UParser import UParser

class TokenGUI:
    def __init__(self, root, file_location):
        self.file_location = file_location

        self.root = root
        self.root.title("Token Analyzer")
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=2)
        root.rowconfigure(1, weight=2)

        self.editor = scrolledtext.ScrolledText(width=80, height=20)
        self.editor.grid(row=0, column=0, padx=2, pady=5, sticky="nsew")

        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky="nsew")

        # Pestaña para el análisis del lexer
        self.lexer_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.lexer_tab, text='Lexer')

        self.treeview = ttk.Treeview(self.lexer_tab, columns=("Word", "Token", "Line"), show="headings")
        self.treeview.heading("Word", text="Word")
        self.treeview.heading("Token", text="Token")
        self.treeview.heading("Line", text="Line")
        self.treeview.pack(expand=True, fill='both')

        # Pestaña para la visualización del análisis sintáctico
        self.parser_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.parser_tab, text='Parser')

        self.syntax_tree = ttk.Treeview(self.parser_tab)
        self.syntax_tree.pack(expand=True, fill='both')

        self.button_analyze = tk.Button(root, text="Analyze", command=self.analyze_file)
        self.button_analyze.grid(row=2, column=0, padx=5, pady=5)

        self.console = tk.Text(root, height=5, bg='#000', fg='#fff')
        self.console.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    def analyze_file(self):
        text = self.editor.get("1.0", tk.END)
        if text:
            # LEXER
            lexer = Lexer(text)
            lexer.run()
            tokens = lexer.get_tokens()
            self.display_tokens(tokens)
            # PARSER
            parser = UParser(tokens)
            parser.RULE_PROGRAM()
            self.display_tokens(tokens)
            self.display_syntax_analysis(parser.syntax_tree)
        else:
            messagebox.showerror("File Not Found", f"File {self.file_location} not found.")

    def display_tokens(self, tokens):
        frequency = {}
        unique_tokens = []
        tokens_lines = []
        self.console.delete("1.0", tk.END)
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for token in tokens:
            self.treeview.insert("", "end", values=(token.get_word(), token.get_token(), token.get_line()))
            unique_tokens.append(token.get_token())
            tokens_lines.append(token.get_line())

        for token, line in zip(unique_tokens, tokens_lines):
            if token in frequency:
                if line in frequency[token]:
                    frequency[token][line] += 1
                else:
                    frequency[token][line] = 1
            else:
                frequency[token] = {line: 1}

        for token, lines in frequency.items():
            no_lines = 0
            total_count = 0
            for line, count in lines.items():
                no_lines += 1
                total_count += count
            self.console.insert("end", f"{total_count} {token}s found in {no_lines} lines\n")

    def display_syntax_analysis(self, syntax_tree_data):
        for item in self.syntax_tree.get_children():
            self.syntax_tree.delete(item)

        def insert_tree_data(tree, parent, data):
            for key, value in data.items():
                node_id = tree.insert(parent, "end", text=key)
                if isinstance(value, dict):
                    insert_tree_data(tree, node_id, value)
                else:
                    tree.insert(node_id, "end", text=value)

        insert_tree_data(self.syntax_tree, "", syntax_tree_data)
