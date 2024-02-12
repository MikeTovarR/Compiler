from Lexer import Lexer

def main():
    lexer = Lexer("/hola(*)'pvto.s'a'")
    lexer.run()
    tokens = lexer.get_tokens()

    for token in tokens:
        print(f"Word: {token.get_word()} Token: {token.get_token()}") 

################## It works by now, we need to define the "ultimate states" to define the last state of a word

if __name__ == "__main__":
    main()