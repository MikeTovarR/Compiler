import tkinter
from TokenGUI import TokenGUI


def main():

    root = tkinter.Tk()
    TokenGUI(root)
    root.mainloop()

################## It works by now, we need to define the "ultimate states" to define the last state of a word

if __name__ == "__main__":
    main()