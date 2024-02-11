class Token:
    def __init__(self, word, token, line):
        self.word = word
        self.token = token
        self.line = line

    def get_word(self):
        return self.word

    def set_word(self, word):
        self.word = word

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token

    def get_line(self):
        return self.line

    def set_line(self, line):
        self.line = line