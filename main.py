import tkinter
from TokenGUI import TokenGUI
from TokenNOGUI import TokenNOGUI

def main():

    file_location = "test.txt" 

    # No GUI version
    TokenNOGUI(file_location)

    # GUI version
    #root = tkinter.Tk()
    #TokenGUI(root, file_location)
    #root.mainloop()

################## It works by now, we need to define the "ultimate states" to define the last state of a word

if __name__ == "__main__":
    main()