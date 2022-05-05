import math
from tkinter import *
from tkinter.filedialog import askopenfilename

import Underlyinglogic
import DebugGUI


class MainGUI(Frame):
    global backend
    def __init__(self):
        super().__init__()
        global inputBinEntry
        global inputHexEntry

        global rightRightStateBoxFrame
        global leftRightStateBoxFrame


        global cpuHzEntry
        global addrTextEntry
        global contentTextEntry
        global debugConsoleOutput



        lowFrame = Frame(self.master, width=200, height=100, bg='#00BFFF')
        lowFrame.grid(row=1, column=1, sticky="s")
        upFrame = Frame(self.master, width=800, height=300, bg='#00BFFF')
        upFrame.grid(row=0, column=0, columnspan=2, sticky="n")

        lowleftFrame = Frame(lowFrame, width=350, height=200, bg='#00BFFF')
        lowleftFrame.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        lowrightFrame = Frame(lowFrame, width=350, height=200, bg='#00BFFF')
        lowrightFrame.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        leftFrame = Frame(upFrame, width=350, height=200, bg='#00BFFF')
        leftFrame.grid(row=0, column=0, padx=5, pady=5)
        leftButtonFrame = Frame(leftFrame, width=30, height=200, bg='#00BFFF')
        leftButtonFrame.grid(row=0, column=2, pady=5, sticky="n")
        leftLableFrame = Frame(leftFrame, width=30, height=200, bg='#00BFFF')
        leftLableFrame.grid(row=0, column=0, pady=5, sticky="n")
        leftRightStateBoxFrame = Frame(leftFrame, width=300, height=200, bg='#00BFFF')
        leftRightStateBoxFrame.grid(row=0, column=1, padx=5, pady=5, sticky="n")

        rightFrame = Frame(upFrame, width=350, height=300, bg='#00BFFF')
        rightFrame.grid(row=0, column=1, padx=5, pady=5, sticky="n")
        rightButtonFrame = Frame(rightFrame, width=30, height=300, bg='#00BFFF')
        rightButtonFrame.grid(row=0, column=2, sticky="n")
        rightLableFrame = Frame(rightFrame, width=30, height=300, bg='#00BFFF')
        rightLableFrame.grid(row=0, column=0, sticky="n")
        rightRightStateBoxFrame = Frame(rightFrame, width=300, height=200, bg='#00BFFF')
        rightRightStateBoxFrame.grid(row=0, column=1, padx=5, pady=5, sticky="n")

        lblgpr0 = Label(leftLableFrame, text="GPR0", width=4, height=1, bg="#08e8ea")
        lblgpr0.grid(row=0, column=0, sticky="n")
        lblgpr1 = Label(leftLableFrame, text="GPR1", width=4, height=1, bg="#08e8ea")
        lblgpr1.grid(row=1, column=0, pady=5, sticky="n")
        lblgpr2 = Label(leftLableFrame, text="GPR2", width=4, height=1, bg="#08e8ea")
        lblgpr2.grid(row=2, column=0, pady=3, sticky="n")
        lblgpr3 = Label(leftLableFrame, text="GPR3", width=4, height=1, bg="#08e8ea")
        lblgpr3.grid(row=3, column=0, pady=4, sticky="n")
        lblixr1 = Label(leftLableFrame, text="IXR1", width=4, height=1, bg="#08e8ea")
        lblixr1.grid(row=4, column=0, pady=3, sticky="n")
        lblixr2 = Label(leftLableFrame, text="IXR2", width=4, height=1, bg="#08e8ea")
        lblixr2.grid(row=5, column=0, pady=3, sticky="n")
        lblixr3 = Label(leftLableFrame, text="IXR3", width=4, height=1, bg="#08e8ea")
        lblixr3.grid(row=6, column=0, pady=3, sticky="n")

        lbl1 = Label(rightLableFrame, text="PC", width=4, height=1, bg="#08e8ea")
        lbl1.grid(row=0, column=0, pady=4, sticky="n")

        lbl2 = Label(rightLableFrame, text="MAR", width=4, height=1, bg="#08e8ea")
        lbl2.grid(row=1, column=0, pady=4, sticky="n")

        lbl3 = Label(rightLableFrame, text="MBR", width=4, height=1, bg="#08e8ea")
        lbl3.grid(row=2, column=0, pady=4, sticky="n")

        lbl4 = Label(rightLableFrame, text="IR", width=4, height=1, bg="#08e8ea")
        lbl4.grid(row=3, column=0, pady=4, sticky="n")

        lbl5 = Label(rightLableFrame, text="MFR", width=4, height=1, bg="#08e8ea")
        lbl5.grid(row=4, column=0, pady=4, sticky="n")
        lbl6 = Label(rightLableFrame, text="CC", width=4, height=1, bg="#08e8ea")
        lbl6.grid(row=5, column=0, pady=4, sticky="n")

        haltcheck = Checkbutton(lowrightFrame, bg='#00BFFF')
        haltcheck.grid(row=0, column=0, padx=0, pady=0)
        runningcheck = Checkbutton(lowrightFrame, bg='#00BFFF')
        runningcheck.grid(row=1, column=0, padx=0, pady=0)
        lbl7 = Label(lowrightFrame, text="Halt", width=4, height=1)
        lbl7.grid(row=0, column=1, padx=10, pady=10)
        lbl8 = Label(lowrightFrame, text="running", width=5, height=1)
        lbl8.grid(row=1, column=1, padx=10, pady=10)

        storeButton = Button(lowrightFrame, text="Store", justify='center', command=self.store)
        storeButton.grid(row=0, column=2, padx=10, pady=10)
        storePlusButton = Button(lowrightFrame, text="Store+",justify='center', command=self.storePlus)
        storePlusButton.grid(row=0, column=3, padx=10, pady=10)
        loadButton = Button(lowrightFrame, text="Load",justify='center', command=self.load)
        loadButton.grid(row=0, column=4, padx=10, pady=10)
        IPLButton = Button(lowrightFrame, text="IPL",justify='center', command=self.ipl)
        IPLButton.grid(row=0, column=5, padx=10, pady=10)
        prog1Button = Button(lowrightFrame, text="Program1",justify='center', command=self.prog1)
        prog1Button.grid(row=0, column=6, padx=10, pady=10, sticky="n")
        prog2Button = Button(lowrightFrame, text="Program2", justify='center', command=self.prog2)
        prog2Button.grid(row=2, column=6, padx=10, pady=10, sticky="n")
        prog3Button = Button(lowrightFrame, text="Program3", justify='center', command=self.prog3)
        prog3Button.grid(row=2, column=4, padx=10, pady=10, sticky="n")
        runButton = Button(lowrightFrame, text="Run",justify='center', command=self.run)
        runButton.grid(row=1, column=2, padx=10, pady=10)
        stopButton = Button(lowrightFrame, text="Stop",justify='center', command=self.stop)
        stopButton.grid(row=1, column=3, padx=10, pady=10)
        singleStepButton = Button(lowrightFrame, text="Single Step",justify='center', command=self.singleStep)
        singleStepButton.grid(row=1, column=4,columnspan=2, padx=10, pady=10)
        singleInstructionButton = Button(lowrightFrame, text="Single Instruction",justify='center', command=self.singleInstruction)
        singleInstructionButton.grid(row=1, column=6, padx=10, pady=10, sticky="n")

        inputBinEntry = Entry(lowleftFrame, width=20, justify='center')
        inputBinEntry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        inputHexEntry = Entry(lowleftFrame, width=20, justify='center')
        inputHexEntry.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        lblbin = Label(lowleftFrame, text="Binary", width=4, height=1, bg="#08e8ea",justify='center')
        lblbin.grid(row=0, column=0, pady=4, sticky="w")
        lblhex = Label(lowleftFrame, text="Heximal", width=5, height=1, bg="#08e8ea",justify='center')
        lblhex.grid(row=0, column=2, pady=4, sticky="w")

        inputBinButton = Button(lowleftFrame, text="inputBin",justify='center', command=self.inputBin)
        inputBinButton.grid(row=1, column=1, padx=10, pady=10)
        inputHexButton = Button(lowleftFrame, text="inputHex",justify='center', command=self.inputHex)
        inputHexButton.grid(row=1, column=3, padx=10, pady=10)



        for i in range(4):
            gprLDButton = Button(leftButtonFrame, text="gprLD", width=4, height=1, command=lambda i =i: self.GPRLD(i))
            gprLDButton.grid(row=i, column=0, pady=4, sticky="n")
        for i in range(3):
            ixrLDButton = Button(leftButtonFrame, text="ixrLD", width=4, height=1, command=lambda i =i: self.IXRLD(i))
            ixrLDButton.grid(row=4 + i, column=0, pady=4, sticky="s")



        pcLDButton = Button(rightButtonFrame, text="pcLD", width=4, height=1, command=self.PCLD)
        pcLDButton.grid(row=0, column=0, pady=5, sticky="n")
        marLDButton = Button(rightButtonFrame, text="marLD", width=4, height=1, command=self.MARLD)
        marLDButton.grid(row=1, column=0, pady=5, sticky="n")
        mbrLDButton = Button(rightButtonFrame, text="mbrLD", width=4, height=1, command=self.MBRLD)
        mbrLDButton.grid(row=2, column=0, pady=5, sticky="n")



        self.ccBinEntry = Entry(rightRightStateBoxFrame, width=8)
        self.ccBinEntry.grid(row=5, column=0, sticky="e")
        self.ccBinEntry.delete(0, END)
        self.ccBinEntry.insert(0, '0000')
        self.irBinEntry = Entry(rightRightStateBoxFrame, width=32)
        self.irBinEntry.grid(row=3, column=0, sticky="e")
        self.irBinEntry.delete(0, END)
        self.irBinEntry.insert(0, '0000000000000000')
        self.marBinEntry = Entry(rightRightStateBoxFrame, width=24)
        self.marBinEntry.grid(row=1, column=0, sticky="e")
        self.marBinEntry.delete(0, END)
        self.marBinEntry.insert(0, '000000000000')
        self.mbrBinEntry = Entry(rightRightStateBoxFrame, width=32)
        self.mbrBinEntry.grid(row=2, column=0, sticky="e")
        self.mbrBinEntry.delete(0, END)
        self.mbrBinEntry.insert(0, '0000000000000000')
        self.mfrBinEntry = Entry(rightRightStateBoxFrame, width=8)
        self.mfrBinEntry.grid(row=4, column=0, sticky="e")
        self.mfrBinEntry.delete(0, END)
        self.mfrBinEntry.insert(0, '0000')
        self.pcBinEntry = Entry(rightRightStateBoxFrame, width=24)
        self.pcBinEntry.grid(row=0, column=0, sticky="e")
        self.pcBinEntry.delete(0, END)
        self.pcBinEntry.insert(0, '000000000000')

        self.gpr0BinEntry = Entry(leftRightStateBoxFrame, width=32)
        self.gpr0BinEntry.grid(row=0, column=0)
        self.gpr0BinEntry.delete(0, END)
        self.gpr0BinEntry.insert(0, '0000000000000000')
        self.gpr1BinEntry = Entry(leftRightStateBoxFrame, width=32)
        self.gpr1BinEntry.grid(row=1, column=0)
        self.gpr1BinEntry.delete(0, END)
        self.gpr1BinEntry.insert(0, '0000000000000000')
        self.gpr2BinEntry = Entry(leftRightStateBoxFrame, width=32)
        self.gpr2BinEntry.grid(row=2, column=0)
        self.gpr2BinEntry.delete(0, END)
        self.gpr2BinEntry.insert(0, '0000000000000000')
        self.gpr3BinEntry = Entry(leftRightStateBoxFrame, width=32)
        self.gpr3BinEntry.grid(row=3, column=0)
        self.gpr3BinEntry.delete(0, END)
        self.gpr3BinEntry.insert(0, '0000000000000000')

        self.ixr1BinEntry = Entry(leftRightStateBoxFrame, width=32)
        self.ixr1BinEntry.grid(row=4, column=0)
        self.ixr1BinEntry.delete(0, END)
        self.ixr1BinEntry.insert(0, '0000000000000000')
        self.ixr2BinEntry = Entry(leftRightStateBoxFrame, width=32)
        self.ixr2BinEntry.grid(row=5, column=0)
        self.ixr2BinEntry.delete(0, END)
        self.ixr2BinEntry.insert(0, '0000000000000000')
        self.ixr3BinEntry = Entry(leftRightStateBoxFrame, width=32)
        self.ixr3BinEntry.grid(row=6, column=0)
        self.ixr3BinEntry.delete(0, END)
        self.ixr3BinEntry.insert(0, '0000000000000000')

        self.ccHexEntry = Entry(rightRightStateBoxFrame, width=2)
        self.ccHexEntry.grid(row=5, column=1, sticky="e")
        self.ccHexEntry.delete(0, END)
        self.ccHexEntry.insert(0, '0')
        self.irHexEntry = Entry(rightRightStateBoxFrame, width=8)
        self.irHexEntry.grid(row=3, column=1, sticky="e")
        self.irHexEntry.delete(0, END)
        self.irHexEntry.insert(0, '0000')
        self.marHexEntry = Entry(rightRightStateBoxFrame, width=8)
        self.marHexEntry.grid(row=1, column=1, sticky="e")
        self.marHexEntry.delete(0, END)
        self.marHexEntry.insert(0, '0000')
        self.mbrHexEntry = Entry(rightRightStateBoxFrame, width=8)
        self.mbrHexEntry.grid(row=2, column=1, sticky="e")
        self.mbrHexEntry.delete(0, END)
        self.mbrHexEntry.insert(0, '0000')
        self.mfrHexEntry = Entry(rightRightStateBoxFrame, width=2)
        self.mfrHexEntry.grid(row=4, column=1, sticky="e")
        self.mfrHexEntry.delete(0, END)
        self.mfrHexEntry.insert(0, '0')
        self.pcHexEntry = Entry(rightRightStateBoxFrame, width=8)
        self.pcHexEntry.grid(row=0, column=1, sticky="e")
        self.pcHexEntry.delete(0, END)
        self.pcHexEntry.insert(0, '0000')

        self.gpr0HexEntry = Entry(leftRightStateBoxFrame, width=8)
        self.gpr0HexEntry.grid(row=0, column=1)
        self.gpr0HexEntry.delete(0, END)
        self.gpr0HexEntry.insert(0, '0000')
        self.gpr1HexEntry = Entry(leftRightStateBoxFrame, width=8)
        self.gpr1HexEntry.grid(row=1, column=1)
        self.gpr1HexEntry.delete(0, END)
        self.gpr1HexEntry.insert(0, '0000')
        self.gpr2HexEntry = Entry(leftRightStateBoxFrame, width=8)
        self.gpr2HexEntry.grid(row=2, column=1)
        self.gpr2HexEntry.delete(0, END)
        self.gpr2HexEntry.insert(0, '0000')
        self.gpr3HexEntry = Entry(leftRightStateBoxFrame, width=8)
        self.gpr3HexEntry.grid(row=3, column=1)
        self.gpr3HexEntry.delete(0, END)
        self.gpr3HexEntry.insert(0, '0000')

        self.ixr1HexEntry = Entry(leftRightStateBoxFrame, width=8)
        self.ixr1HexEntry.grid(row=4, column=1)
        self.ixr1HexEntry.delete(0, END)
        self.ixr1HexEntry.insert(0, '0000')
        self.ixr2HexEntry = Entry(leftRightStateBoxFrame, width=8)
        self.ixr2HexEntry.grid(row=5, column=1)
        self.ixr2HexEntry.delete(0, END)
        self.ixr2HexEntry.insert(0, '0000')
        self.ixr3HexEntry = Entry(leftRightStateBoxFrame, width=8)
        self.ixr3HexEntry.grid(row=6, column=1)
        self.ixr3HexEntry.delete(0, END)
        self.ixr3HexEntry.insert(0, '0000')


        # downUpFrame = Frame(self.master, width=800, height=300, bg='#00BFFF')
        # downUpFrame.grid(row=3, column=0)
        # #downUpFrame = Toplevel()
        # #downUpFrame.geometry("800x800")
        # #downUpFrame.title("toplevel")
        #
        # debugConsoleOutput = Text(downUpFrame, width=50)
        # debugConsoleOutput.grid(row=3, column=1)
        # cpuHzEntry = Entry(downUpFrame, width=50)
        # cpuHzEntry.grid(row=0, column=1)
        # addrTextEntry = Entry(downUpFrame, width=32)
        # addrTextEntry.grid(row=1, column=1)
        # contentTextEntry = Entry(downUpFrame, width=32)
        # contentTextEntry.grid(row=1, column=3)
        #
        # setButton = Button(downUpFrame, text="Set", command=self.set)
        # setButton.grid(row=0, column=2)
        # loadButton = Button(downUpFrame, text="loadMemory", command=self.loadMemory)
        # loadButton.grid(row=1, column=4)
        # storeButton = Button(downUpFrame, text="storeMemory", command=self.storeMemory)
        # storeButton.grid(row=1, column=5)
        # readCacheButton = Button(downUpFrame, text="Print", command=self.printCache)
        # readCacheButton.grid(row=2, column=2)
        # flushCacheButton = Button(downUpFrame, text="Flush Cache", command=self.flushCache)
        # flushCacheButton.grid(row=2, column=3)
        #
        # #downUpFrame.mainloop()



    def run(self):
        global backend
        self.backend.start()

    def ipl(self):
        global backend
        self.backend.loadProgram("IPL.txt")

    def singleStep(self):
        global backend
        self.backend.runsinglestep()
        self.backend.debugGuiPrint("Running single step")

    def singleInstruction(self):
        global backend
        global inputHexEntry
        self.backend.runSingleInstruction(int(inputHexEntry.get(), base=16))
        self.backend.debugGuiPrint("Running single instruction")

    def store(self):
        global backend
        self.backend.memoryWrite(self.backend.mar, self.backend.mbr)
        self.backend.cache.flush()
        self.renew()
        self.backend.debugGuiPrint("Running Store, store {0:d} to {1:X}".format(self.backend.mbr, self.backend.mar))

    def storePlus(self):
        global backend
        self.backend.memoryWrite(self.backend.mar, self.backend.mbr)
        self.backend.cache.flush()
        self.backend.pc += 1
        self.renew()
        self.backend.debugGuiPrint("Running Store+, store {0:d} to {1:X}".format(self.backend.mbr, self.backend.mar))

    def load(self):
        global backend
        self.backend.mbr = self.backend.memoryRead(self.backend.mar)
        self.renew()
        self.backend.debugGuiPrint("Running Load, read {0:d} to {1:X}".format(self.backend.mbr, self.backend.mar))

    def prog1(self):

        self.backend.reset()
        file_addr = askopenfilename()
        self.backend.loadProgram(file_addr)
        self.backend.pc = 0x100
        self.backend.cache.flush()
        self.renew()
        self.backend.debugGuiPrint("PC Set to 0x100")

    def prog2(self):

        self.backend.reset()
        file_addr = askopenfilename()
        self.backend.loadProgram(file_addr)
        self.backend.pc = 0x200
        self.backend.cache.flush()
        self.renew()
        self.backend.debugGuiPrint("PC Set to 0x200")

    def prog3(self):

        self.backend.reset()
        file_addr = askopenfilename()
        self.backend.loadProgram(file_addr)
        self.backend.pc = 0x6
        self.backend.cache.flush()
        self.renew()
        self.backend.debugGuiPrint("PC Set to 0x6")

    def stop(self):
        global backend
        self.backend.stop()

    def inputBin(self):
        global inputBinEntry
        global inputHexEntry
        #global debugGUI
        try:
            inputValue = int(inputBinEntry.get(), base=2)
            inputHexEntry.delete(0, END)
            inputHexEntry.insert(0, "{0:X}".format(inputValue))
        except (TypeError, ValueError):
            inputHexEntry.delete(0, END)
            inputBinEntry.delete(0, END)
            inputHexEntry.insert(0, "")
            inputHexEntry.insert(0, "")
            self.debugGUI.debugGuiPrint("Invalid binary input")

    def inputHex(self):
        global inputBinEntry
        global inputHexEntry
        #global debugGUI
        try:
            inputValue = int(inputHexEntry.get(), base=16)
            inputBinEntry.delete(0, END)
            inputBinEntry.insert(0, "{0:b}".format(inputValue))
        except (TypeError, ValueError):
            inputHexEntry.delete(0, END)
            inputBinEntry.delete(0, END)
            inputHexEntry.insert(0, "")
            inputHexEntry.insert(0, "")
            self.debugGUI.debugGuiPrint("Invalid binary input")

    def GPRLD(self, i):
        global inputBinEntry
        global inputHexEntry
        global backend
        if inputBinEntry.get() == "":
            inputValue = int(inputHexEntry.get(), base=16)
        else:
            inputValue = int(inputBinEntry.get(), base=2)
        if inputValue > int(math.pow(2, 16) - 1) | inputValue < 0:
            self.debugGUI.debugGuiPrint("Input is invalid for GPR" + i)
            return
        self.backend.gpr[i] = inputValue
        self.renew()

    def IXRLD(self, i):
        global inputBinEntry
        global inputHexEntry
        global backend
        if inputBinEntry.get() == "":
            inputValue = int(inputHexEntry.get(), base=16)
        else:
            inputValue = int(inputBinEntry.get(), base=2)
        if inputValue > int(math.pow(2, 16) - 1) | inputValue < 0:
            self.debugGUI.debugGuiPrint("Input is invalid for IXR" + i)
            return
        self.backend.ixr[i] = inputValue
        self.renew()

    def PCLD(self):
        global inputBinEntry
        global inputHexEntry
        global backend
        if inputBinEntry.get() == "":
            inputValue = int(inputHexEntry.get(), base=16)
        else:
            inputValue = int(inputBinEntry.get(), base=2)
        if inputValue > int(math.pow(2, 12) - 1) | inputValue < 0:
            self.debugGUI.debugGuiPrint("Input is invalid for PC")
            return
        self.backend.pc = inputValue
        self.renew()

    def MARLD(self):
        global inputBinEntry
        global inputHexEntry

        if inputBinEntry.get() == "":
            inputValue = int(inputHexEntry.get(), base=16)
        else:
            inputValue = int(inputBinEntry.get(), base=2)
        if inputValue > int(math.pow(2, 12) - 1) | inputValue < 0:
            self.debugGUI.debugGuiPrint("Input is invalid for MAR")
            return
        self.backend.mar = inputValue
        self.renew()

    def MBRLD(self):
        global inputBinEntry
        global inputHexEntry
        global backend
        if inputBinEntry.get() == "":
            inputValue = int(inputHexEntry.get(), base=16)
        else:
            inputValue = int(inputBinEntry.get(), base=2)
        if inputValue > int(math.pow(2, 16) - 1) | inputValue < 0:
            self.debugGUI.debugGuiPrint("Input is invalid for MBR")
            return
        self.backend.mbr = inputValue
        self.renew()

    def bindUnderlyinglogic(self, backEnd : Underlyinglogic):
        self.backend = backEnd

    def bindDebugGUI(self, debuggui : DebugGUI):
        self.debugGUI = debuggui

    def renew(self):
        global rightRightStateBoxFrame
        global leftRightStateBoxFrame
        global backend
        global ccBinEntry
        self.ccBinEntry.delete(0, END)
        self.ccBinEntry.insert(0, "{0:4b}".format(self.backend.cc).replace(' ', '0'))
        global irBinEntry
        self.irBinEntry.delete(0, END)
        self.irBinEntry.insert(0, "{0:16b}".format(self.backend.ir).replace(' ', '0'))
        global marBinEntry
        self.marBinEntry.delete(0, END)
        self.marBinEntry.insert(0, "{0:12b}".format(self.backend.mar).replace(' ', '0'))
        global mbrBinEntry
        self.mbrBinEntry.delete(0, END)
        self.mbrBinEntry.insert(0, "{0:16b}".format(self.backend.mbr).replace(' ', '0'))
        global mfrBinEntry
        self.mfrBinEntry.delete(0, END)
        self.mfrBinEntry.insert(0, "{0:4b}".format(self.backend.mfr).replace(' ', '0'))
        global pcBinEntry
        self.pcBinEntry.delete(0, END)
        self.pcBinEntry.insert(0, "{0:12b}".format(self.backend.pc).replace(' ', '0'))
        global gpr0BinEntry
        self.gpr0BinEntry.delete(0, END)
        self.gpr0BinEntry.insert(0, "{0:16b}".format(self.backend.gpr[0]).replace(' ', '0'))
        global gpr1BinEntry
        self.gpr1BinEntry.delete(0, END)
        self.gpr1BinEntry.insert(0, "{0:16b}".format(self.backend.gpr[1]).replace(' ', '0'))
        global gpr2BinEntry
        self.gpr2BinEntry.delete(0, END)
        self.gpr2BinEntry.insert(0, "{0:16b}".format(self.backend.gpr[2]).replace(' ', '0'))
        global gpr3BinEntry
        self.gpr3BinEntry.delete(0, END)
        self.gpr3BinEntry.insert(0, "{0:16b}".format(self.backend.gpr[3]).replace(' ', '0'))
        global ixr1BinEntry
        self.ixr1BinEntry.delete(0, END)
        self.ixr1BinEntry.insert(0, "{0:16b}".format(self.backend.ixr[0]).replace(' ', '0'))
        global ixr2BinEntry
        self.ixr2BinEntry.delete(0, END)
        self.ixr2BinEntry.insert(0, "{0:16b}".format(self.backend.ixr[1]).replace(' ', '0'))
        global ixr3BinEntry
        self.ixr3BinEntry.delete(0, END)
        self.ixr3BinEntry.insert(0, "{0:16b}".format(self.backend.ixr[2]).replace(' ', '0'))


        self.ccHexEntry.delete(0, END)
        self.ccHexEntry.insert(0, "{0:1X}".format(self.backend.cc).replace(' ', '0'))

        self.irHexEntry.delete(0, END)
        self.irHexEntry.insert(0, "{0:4X}".format(self.backend.ir).replace(' ', '0'))

        self.marHexEntry.delete(0, END)
        self.marHexEntry.insert(0, "{0:4X}".format(self.backend.mar).replace(' ', '0'))

        self.mbrHexEntry.delete(0, END)
        self.mbrHexEntry.insert(0, "{0:4X}".format(self.backend.mbr).replace(' ', '0'))

        self.mfrHexEntry.delete(0, END)
        self.mfrHexEntry.insert(0, "{0:1X}".format(self.backend.mfr).replace(' ', '0'))

        self.pcHexEntry.delete(0, END)
        self.pcHexEntry.insert(0, "{0:4X}".format(self.backend.pc).replace(' ', '0'))


        self.gpr0HexEntry.delete(0, END)
        self.gpr0HexEntry.insert(0, "{0:4X}".format(self.backend.gpr[0]).replace(' ', '0'))

        self.gpr1HexEntry.delete(0, END)
        self.gpr1HexEntry.insert(0, "{0:4X}".format(self.backend.gpr[1]).replace(' ', '0'))

        self.gpr2HexEntry.delete(0, END)
        self.gpr2HexEntry.insert(0, "{0:4X}".format(self.backend.gpr[2]).replace(' ', '0'))

        self.gpr3HexEntry.delete(0, END)
        self.gpr3HexEntry.insert(0, "{0:4X}".format(self.backend.gpr[3]).replace(' ', '0'))


        self.ixr1HexEntry.delete(0, END)
        self.ixr1HexEntry.insert(0, "{0:4X}".format(self.backend.ixr[0]).replace(' ', '0'))

        self.ixr2HexEntry.delete(0, END)
        self.ixr2HexEntry.insert(0, "{0:4X}".format(self.backend.ixr[1]).replace(' ', '0'))

        self.ixr3HexEntry.delete(0, END)
        self.ixr3HexEntry.insert(0, "{0:4X}".format(self.backend.ixr[2]).replace(' ', '0'))




    # def flushCache(self):
    #     global backend
    #     self.backend.cache.flush()
    #     self.debugGuiPrint("Cache Flushed")
    #
    # def set(self):
    #     global cpuHzEntry
    #     global backend
    #     Hz = int(cpuHzEntry.get())
    #     self.backend.setHz(Hz)
    #     self.debugGuiPrint("CPU Hz set to {0:d}".format(Hz))
    #
    # def loadMemory(self):
    #     global addrTextEntry
    #     global contentTextEntry
    #     global backend
    #     addr = int(addrTextEntry.get(), base=16)
    #     self.backend.cache.flush()
    #     contentTextEntry.delete(0, END)
    #     contentTextEntry.insert(0, "{0:X}".format(self.backend.memory.load(addr)))
    #     self.debugGuiPrint("Load memory at {0:X}, content is {1:X}".format(addr, self.backend.memory.load(addr)))
    #
    # def storeMemory(self):
    #     global addrTextEntry
    #     global contentTextEntry
    #     global backend
    #     addr = int(addrTextEntry.get(), base=16)
    #     content = int(contentTextEntry.get(), base=16)
    #     self.backend.cache.flush()
    #     self.backend.memory.store(addr, content)
    #     self.debugGuiPrint("Set memory at {0:X} to {1:X}".format(addr, content))
    #
    # def debugGuiPrint(self, s):
    #     global debugConsoleOutput
    #     debugConsoleOutput.insert(END, s)
    #     debugConsoleOutput.insert(END, "\n")
    #
    # def printCache(self):
    #     global backend
    #     self.debugGuiPrint("Cache: current size: {0:d}, max size: {0:d}".format(len(self.backend.cache.addrList), self.backend.cache.max_value))
    #     i = 0
    #     while (i < len(self.backend.cache.addrList)):
    #         self.debugGuiPrint("Addr {0:X} Content {1:X}".format(self.backend.cache.addrList[i], self.backend.cache.contentList[i]))
    #         i += 1











