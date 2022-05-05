
import threading
import time
import traceback
import DebugGUI
import IOGUI
from Cache import Cache
from ImplementInstruction import ImplementInstruction
from Instruction import Instruction
from Memory import Memory
import GUI

class Underlyinglogic:
    global ir
    global mar
    global mbr
    global mfr
    global pc
    global cc
    global halted
    global running
    global debug
    global HZ
    global cache
    global memory
    global isa
    gpr = []
    ixr = []
    def __init__(self):
        global gpr
        global ixr
        global ir
        global mar
        global mbr
        global mfr
        global pc
        global cc
        global halted
        global running
        global debug
        global HZ
        global cache
        global memory
        global isa
        self.isa = ImplementInstruction(self)
        self.memory = Memory(4096)
        self.cache = Cache(16, self)
        self.gpr = [0, 0, 0, 0]
        self.ixr = [0, 0, 0]
        self.fr = ["", ""]
        self.ir = 0
        self.mar = 0
        self.mbr = 0
        self.mfr = 0
        self.pc = 0
        self.cc = 0
        self.debug = True
        self.HZ = 1000

    def bindGUI(self, mainGUI : GUI, debugGUI : DebugGUI, ioGUI : IOGUI):
        global maingui
        self.iogui = ioGUI
        self.maingui = mainGUI
        self.debuggui = debugGUI

    def getHz(self):
        return self.HZ

    def setHz(self, Hz):
        global HZ
        self.HZ = Hz

    def simulateDelay(self):
        global HZ
        try:
            time.sleep(1000 / self.HZ)
        except InterruptedError:
            traceback.print_exc()


    def reset(self):
        global gpr
        global ixr
        global ir
        global mar
        global mbr
        global mfr
        global pc
        global cc
        global memory
        self.gpr = [0, 0, 0, 0]
        self.ixr = [0, 0, 0]
        self.ir = 0
        self.mar = 0
        self.mbr = 0
        self.mfr = 0
        self.pc = 0
        self.cc = 0
        self.memory = Memory(4096)

    def loop(self, run):
        self.running = run
        while self.running:
            self.fetch()
            self.maingui.renew()
            self.decode()
            self.maingui.renew()
            self.exe()
            self.maingui.renew()

    def start(self):
        self.halted = False
        self.running = True
        thread1 = threading.Thread(target= Underlyinglogic.loop, args= (self,self.running))
        thread1.start()



    def stop(self):
        global running
        global maingui
        self.running = False
        self.maingui.renew()

    def singleLoop(self, i):
        k = i
        self.fetch()
        self.maingui.renew()
        self.decode()
        self.maingui.renew()
        self.exe()
        self.maingui.renew()

    def runsinglestep(self):
        i = 0
        thread1 = threading.Thread(target=Underlyinglogic.singleLoop, args=(self, i))
        thread1.start()


    def singleInstruction(self, ins):
        global i
        self.i = Instruction(ins)
        self.simulateDelay()
        self.exe()
        self.maingui.renew()

    def runSingleInstruction(self, ins):
        thread1 = threading.Thread(target=Underlyinglogic.singleInstruction, args=(self, ins))
        thread1.start()


    def loadProgram(self, s):
        global memory
        global maingui
        global debuggui
        myFile = open(s, "r")
        try:
            lines = myFile.readlines()
            print(lines)
            for line in lines:
                if line == "":
                    continue
                if line[0] == '#':
                    continue
                addr = int(line[0:4], 16)
                content = int(line[5:9], 16)
                self.memory.store(addr, content)
            string1 = "{} {} {}".format('Program', str(s), 'loaded')
            self.debuggui.debugGuiPrint(string1)
        except IOError:
            string2 = "{} {} {}".format('Program', str(s), 'does not exist')
            self.debuggui.debugGuiPrint(string2)


    def debugGuiPrint(self, s):
        global debug
        global debuggui
        if not self.debug:
            return
        self.debuggui.debugGuiPrint(s)

    def memoryRead(self,addr):
        global mar
        global mbr
        self.mar = addr
        global cache
        global memory
        global debuggui
        self.mbr = self.cache.read(self.mar)
        if self.mbr == -1:
            string1 = "Cache missed at {0:X}".format(self.mar)
            self.debuggui.debugGuiPrint(string1)
            self.mbr = self.memory.load(self.mar)
            self.simulateDelay()
            self.cache.write(self.mar, self.mbr)
        return self.mbr

    def memoryWrite(self, addr, content):
        global mar
        global mbr
        self.mar = addr
        self.mbr = content
        global cache
        global debuggui
        self.cache.write(self.mar, self.mbr)
        string1 = "Write {0:d} to {1:X}".format(content, addr)
        self.debuggui.debugGuiPrint(string1)

    def fetch(self):
        global ir
        global mar
        global pc
        self.mar = self.pc
        self.ir = self.memoryRead(self.mar)
        self.pc += 1
        if self.pc > 4095:
            self.pc = 0
        self.simulateDelay()

    def decode(self):
        global i
        global ir
        self.i = Instruction(self.ir)
        self.simulateDelay()

    def exe(self):
        global cc
        global i
        global isa
        if (4 <= self.i.opcode <= 7) | (16 <= self.i.opcode <= 18) | (25 <= self.i.opcode <= 26):
            self.cc = 0
        if self.i.opcode == 0:
            self.isa.halt()
        elif self.i.opcode == 1:
            self.isa.ldr(self.i)
        elif self.i.opcode == 2:
            self.isa.str(self.i)
        elif self.i.opcode == 3:
            self.isa.lda(self.i)
        elif self.i.opcode == 33:
            self.isa.ldx(self.i)
        elif self.i.opcode == 34:
            self.isa.stx(self.i)
        elif self.i.opcode == 8:
            self.isa.jz(self.i)
        elif self.i.opcode == 9:
            self.isa.jne(self.i)
        elif self.i.opcode == 10:
            self.isa.jcc(self.i)
        elif self.i.opcode == 11:
            self.isa.jma(self.i)
        elif self.i.opcode == 12:
            self.isa.jsr(self.i)
        elif self.i.opcode == 13:
            self.isa.rfs(self.i)
        elif self.i.opcode == 14:
            self.isa.sob(self.i)
        elif self.i.opcode == 15:
            self.isa.jge(self.i)
        elif self.i.opcode == 4:
            self.isa.amr(self.i)
        elif self.i.opcode == 5:
            self.isa.smr(self.i)
        elif self.i.opcode == 6:
            self.isa.air(self.i)
        elif self.i.opcode == 7:
            self.isa.sir(self.i)
        elif self.i.opcode == 16:
            self.isa.mlt(self.i)
        elif self.i.opcode == 17:
            self.isa.dvd(self.i)
        elif self.i.opcode == 18:
            self.isa.trr(self.i)
        elif self.i.opcode == 19:
            self.isa.andd(self.i)
        elif self.i.opcode == 20:
            self.isa.orr(self.i)
        elif self.i.opcode == 21:
            self.isa.nott(self.i)
        elif self.i.opcode == 25:
            self.isa.src(self.i)
        elif self.i.opcode == 26:
            self.isa.rrc(self.i)
        elif self.i.opcode == 49:
            self.isa.inn(self.i)
        elif self.i.opcode == 50:
            self.isa.out(self.i)
        elif self.i.opcode == 51:
            self.isa.chk(self.i)
        elif self.i.opcode == 35:
            self.isa.jgt(self.i)
        elif self.i.opcode == 27:
            self.isa.fadd(self.i)
        elif self.i.opcode == 28:
            self.isa.fsub(self.i)
        elif self.i.opcode == 29:
            self.isa.vadd(self.i)
        elif self.i.opcode == 30:
            self.isa.vsub(self.i)
        elif self.i.opcode == 40:
            self.isa.ldfr(self.i)
        elif self.i.opcode == 41:
            self.isa.stfr(self.i)
        elif self.i.opcode == 31:
            self.isa.cnvrt(self.i)
        elif self.i.opcode == 24:
            if self.i.trapCode > 15 | self.i.trapCode < 0:
                self.mfr |= 1
            else:
                self.isa.trap(self.i)
        else:
            global mfr
            global pc
            self.mfr |= 4
            self.pc = self.memoryRead(1)
            self.debugGuiPrint("Illegal Operation Code")
        self.simulateDelay()













