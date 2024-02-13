from Lexer import Lexer
from File_Handler import FileHandler


def main():

    file = FileHandler('file.txt')
    lexer = Lexer(file.read_file())
    lexer.run()
    tokens = lexer.get_tokens()

    for token in tokens:
        print(f"Word: {token.get_word()} Token: {token.get_token()}") 

################## It works by now, we need to define the "ultimate states" to define the last state of a word

if __name__ == "__main__":
    main()