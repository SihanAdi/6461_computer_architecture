
from tkinter import *

import Underlyinglogic as backEnd

class DebugGUI(Frame):
    def __init__(self):
        super().__init__()


        debugToplevel = Toplevel(self.master, width=800, height=300, bg='#00BFFF')
        debugToplevel.title("debugGUI")
        # downUpFrame = Toplevel()
        # downUpFrame.geometry("800x800")
        # downUpFrame.title("toplevel")

        cpuSpeedLable = Label(debugToplevel, text="Cpu Speed", bg="#08e8ea")
        cpuSpeedLable.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        addressLable = Label(debugToplevel, text="Addr", bg="#08e8ea")
        addressLable.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        valueLable = Label(debugToplevel, text="Value", bg="#08e8ea")
        valueLable.grid(row=1, column=2, padx=10, pady=10, sticky='w')
        outputLable = Label(debugToplevel, text="Output", bg="#08e8ea")
        outputLable.grid(row=3, column=0, padx=10, pady=10, sticky='e')

        self.cpuHzEntry = Entry(debugToplevel, width=43)
        self.cpuHzEntry.grid(row=0, column=1, columnspan=4, sticky='w')
        self.addrTextEntry = Entry(debugToplevel, width=15)
        self.addrTextEntry.grid(row=1, column=1)
        self.contentTextEntry = Entry(debugToplevel, width=15)
        self.contentTextEntry.grid(row=1, column=3)
        self.debugConsoleOutput = Text(debugToplevel, width=55)
        self.debugConsoleOutput.grid(row=3, column=1, columnspan=5, sticky='w')



        self.setButton = Button(debugToplevel, text="Set", command=self.set)
        self.setButton.grid(row=0, column=5)
        self.loadButton = Button(debugToplevel, text="load", command=self.loadMemory)
        self.loadButton.grid(row=1, column=4, padx=10, pady=10)
        self.storeButton = Button(debugToplevel, text="store", command=self.storeMemory)
        self.storeButton.grid(row=1, column=5, padx=10, pady=10)
        self.readCacheButton = Button(debugToplevel, text="Print", command=self.printCache, justify="center")
        self.readCacheButton.grid(row=2, column=1)
        self.flushCacheButton = Button(debugToplevel, text="Flush Cache", command=self.flushCache, justify="center")
        self.flushCacheButton.grid(row=2, column=3)

    def bindUnderlyinglogic(self, back : backEnd.Underlyinglogic):
        self.backend = back

    def flushCache(self):

        self.backend.cache.flush()
        self.debugGuiPrint("Cache Flushed")

    def set(self):

        Hz = int(self.cpuHzEntry.get())
        self.backend.setHz(Hz)
        self.debugGuiPrint("CPU Hz set to {0:d}".format(Hz))

    def loadMemory(self):

        addr = int(self.addrTextEntry.get(), base=16)
        self.backend.cache.flush()
        self.contentTextEntry.delete(0, END)
        self.contentTextEntry.insert(0, "{0:X}".format(self.backend.memory.load(addr)))
        self.debugGuiPrint("Load memory at {0:X}, content is {1:X}".format(addr, self.backend.memory.load(addr)))

    def storeMemory(self):

        addr = int(self.addrTextEntry.get(), base=16)
        content = int(self.contentTextEntry.get(), base=16)
        self.backend.cache.flush()
        self.backend.memory.store(addr, content)
        self.debugGuiPrint("Set memory at {0:X} to {1:X}".format(addr, content))

    def debugGuiPrint(self, s):

        self.debugConsoleOutput.insert(END, s)
        self.debugConsoleOutput.insert(END, "\n")

    def printCache(self):

        self.debugGuiPrint("Cache: current size: {0:d}, max size: {0:d}".format(len(self.backend.cache.addrList),
                                                                             self.backend.cache.max_value))
        i = 0
        while (i < len(self.backend.cache.addrList)):
            self.debugGuiPrint(
                "Addr {0:X} Content {1:X}".format(self.backend.cache.addrList[i], self.backend.cache.contentList[i]))
            i += 1
