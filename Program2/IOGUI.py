
from tkinter import *
import Underlyinglogic

class IOGUI(Frame):
    def __init__(self):
        super().__init__()
        global consoleText
        global crText
        global consoleInputEntry
        global crInputEntry
        global printerText
        IOToplevel = Toplevel(self.master, width=800, height=500, bg='#00BFFF')
        IOToplevel.title("IOGUI")

        inputLable = Label(IOToplevel, text="Input", bg="#08e8ea", justify="center")
        inputLable.grid(row=0, column=1)
        consoleInputLable = Label(IOToplevel, text="Console", bg="#08e8ea")
        consoleInputLable.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        consoleLable = Label(IOToplevel, text="Console ", bg="#08e8ea")
        consoleLable.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        crInputLable = Label(IOToplevel, text="Card Reader", bg="#08e8ea")
        crInputLable.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        crLable = Label(IOToplevel, text="CR ", bg="#08e8ea")
        crLable.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        outputLable = Label(IOToplevel, text="Output", bg="#08e8ea", justify="center")
        outputLable.grid(row=5, column=1)
        consoleprintLable = Label(IOToplevel, text="Console print", bg="#08e8ea")
        consoleprintLable.grid(row=6, column=0, padx=10, pady=10, sticky='w')

        consoleInputEntry = Entry(IOToplevel, width=30)
        consoleInputEntry.grid(row=1, column=1, pady=10, sticky='w')
        consoleText = Text(IOToplevel, width=39, height=1)
        consoleText.grid(row=2, column=1, pady=10, sticky='w')
        crInputEntry = Entry(IOToplevel, width=30)
        crInputEntry.grid(row=3, column=1, pady=10, sticky='w')
        crText = Text(IOToplevel, width=39, height=1)
        crText.grid(row=4, column=1, pady=10, sticky='w')
        printerText = Text(IOToplevel, width=39, height=42)
        printerText.grid(row=6, column=1, pady=10, sticky='w')
        consoleText.insert(END, consoleInputEntry.get())
        consoleText.insert(END, '\0')


        consoleInputButton = Button(IOToplevel, text="Console Keyboard Input", command=self.consoleInput)
        consoleInputButton.grid(row=1, column=2, padx=10, pady=10, sticky='w')
        crInputButton = Button(IOToplevel, text="Card Reader Input", command=self.crInput)
        crInputButton.grid(row=3, column=2, padx=10, pady=10, sticky='w')

    def bindUnderlyinglogic(self, back: Underlyinglogic):
        self.backend = back

    def consoleInput(self):
        global consoleText
        global crText
        global consoleInputEntry
        global crInputEntry
        s = consoleText.get(1.0, END)
        s = s[0:len(s) - 1]
        if s == "\n":
            s = consoleInputEntry.get()
        else:
            s = s + consoleInputEntry.get()
        consoleText.delete(1.0, END)
        consoleText.insert(1.0, s)

    def crInput(self):
        global consoleText
        global crText
        global consoleInputEntry
        global crInputEntry
        crText.insert(END, crInputEntry.get())
        crText.insert(END, '\0')

    def popconsole(self):
        global consoleText
        global crText
        global consoleInputEntry
        global crInputEntry
        s = consoleText.get(1.0, END)
        c = '\0'
        if not s == "\n":
            c = s[0]
            s = s[1 : len(s) - 1]
        consoleText.delete(1.0, END)
        consoleText.insert(END, s)
        return c

    def isconsoleEmpty(self):
        global consoleText
        global crText
        global consoleInputEntry
        global crInputEntry
        s = consoleText.get(1.0, END)
        if s == "":
            return True
        else:
            return False

    def isCREmpty(self):
        global consoleText
        global crText
        global consoleInputEntry
        global crInputEntry
        if crText.get(1.0, END) == "":
            return True
        else:
            return False

    def popCR(self):
        global consoleText
        global crText
        global consoleInputEntry
        global crInputEntry
        s = crText.get(1.0, END)
        c = '\0'
        if s != "":
            c = s[0]
            s = s[1:]
        crText.delete(1.0, END)
        crText.insert(END, s)
        return c

    def pushPrint(self, c):
        global printerText
        s = printerText.get(1.0, END)
        s = s[0:len(s) - 1]
        if s == "\n":
            s = c
        else:
            s = s + c
        printerText.delete(1.0, END)
        printerText.insert(1.0, s)

    def insertPrint(self, c):
        global printerText
        s = printerText.get('1.0', END)
        split = s.split("\n")
        split[len(split) - 2] = c + split[len(split) - 2]
        ns = ""
        for value in split:
            ns += value
            ns += "\n"
        printerText.delete('1.0', END)
        printerText.insert('1.0', ns[0:len(ns) - 1])





