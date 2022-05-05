from tkinter import *

from DebugGUI import DebugGUI
from GUI import MainGUI
from IOGUI import IOGUI
import Underlyinglogic as backEnd

def main():
    backend = backEnd.Underlyinglogic()
    root = Tk()
    root.geometry("1020x350+300+300")
    root.configure(bg='#00BFFF')
    root.title('6441')
    mainGUI = MainGUI()
    debugGUI = DebugGUI()
    ioGUI = IOGUI()
    mainGUI.bindUnderlyinglogic(backend)
    mainGUI.bindDebugGUI(debugGUI)
    debugGUI.bindUnderlyinglogic(backend)
    ioGUI.bindUnderlyinglogic(backend)
    backend.bindGUI(mainGUI, debugGUI, ioGUI)
    root.mainloop()

if __name__ == '__main__':
    main()


