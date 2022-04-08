from tkinter import *

from DebugGUI import DebugGUI
from GUI import MainGUI
from IOGUI import IOGUI
import BackEnd as backEnd

def main():
    backend = backEnd.BackEnd()
    root = Tk()
    root.geometry("990x350+300+300")
    root.configure(bg='#00BFFF')
    root.title('6441')
    mainGUI = MainGUI()
    debugGUI = DebugGUI()
    ioGUI = IOGUI()
    mainGUI.bindBackEnd(backend)
    mainGUI.bindDebugGUI(debugGUI)
    debugGUI.bindBackEnd(backend)
    ioGUI.bindBackEnd(backend)
    backend.bindGUI(mainGUI, debugGUI, ioGUI)
    root.mainloop()

if __name__ == '__main__':
    main()


