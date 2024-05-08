from File_Handler import FileHandler
from Lexer import Lexer
from UParser import UParser

class TokenNOGUI:
    def __init__(self, file_location):
        self.file_location = file_location

        self.analyze_file()

    def analyze_file(self):
        file_handler = FileHandler(self.file_location) ## uncomment this lines and comment the line below to activate the editor
        text = file_handler.read_file()
        if text is not None:
            # LEXER
            lexer = Lexer(text)
            lexer.run()
            tokens = lexer.get_tokens()
            self.display_tokens(tokens)
            # PARSER
            parser = UParser(tokens) # Incluí el parser aquí
            parser.RULE_PROGRAM()
        else:
            print("File Not Found")

    def display_tokens(self, tokens):
        frequency = {}
        unique_tokens = []
        tokens_lines = []

        for token in tokens:
            unique_tokens.append(token.get_token())
            tokens_lines.append( token.get_line())

        for token, line in zip(unique_tokens, tokens_lines):
            if token in frequency:
                if line in frequency[token]:
                    frequency[token][line] += 1
                else: frequency[token][line] = 1
            else:
                frequency[token] = {line: 1}

        for token, lines in frequency.items():
            no_lines = 0
            total_count = 0
            for line, count in lines.items():
                no_lines += 1
                total_count += count
            print(f"{total_count} {token}s found in {no_lines} lines\n") #dont print well, try with lines first
                
