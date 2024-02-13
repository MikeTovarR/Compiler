import os

class FileHandler:
    def __init__(self, location):
        self.location = location
        self.lines = []

    def read_file(self):
        if os.path.exists(self.location):
            with open(self.location, "r") as file:
                lines = file.read()
            return lines
        else:
            print(f'File {self.location} not found')
            return