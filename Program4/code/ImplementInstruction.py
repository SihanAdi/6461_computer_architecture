import Underlyinglogic
import Instruction as Ins
import math
import struct

class ImplementInstruction:
    global backend

    def __init__(self, backEnd : Underlyinglogic):
        global backend
        self.backend = backEnd

    def computeEA(self, i: Ins.Instruction):
        global backend
        if i.indirect == 0:
            if i.ixrIndex >= 0:
                return i.addr + self.backend.ixr[i.ixrIndex]
            else:
                return i.addr
        else:
            if i.ixrIndex >= 0:
                return self.backend.memoryRead(i.addr) + self.backend.memoryRead(self.backend.ixr[i.ixrIndex])
            else:
                return self.backend.memoryRead(i.addr)

    def computeIXREA(self, i: Ins.Instruction):
        global backend
        if i.indirect == 0:
            return i.addr
        else:
            return self.backend.memoryRead(i.addr)

    def halt(self):
        global backend
        self.backend.running = False
        self.backend.halted = True
        self.backend.debugGuiPrint("Running Halt")

    #def trap(self, i: Instruction):
        #backend.memoryWrite(2, backend.pc + 1)
        #backend.pc = backend.memoryRead(backend.memoryRead(0) + i.trapCode)
        #backend.debugGuiPrint("Running TRAP")

    def ldr(self, i: Ins.Instruction):
        global backend
        self.backend.debugGuiPrint("Running LDR")
        ea = self.computeEA(i)
        if ea > 2048:
            self.backend.mfr |= 8
            self.backend.debugGuiPrint("Illegal Memory Address beyond 2048")
            self.backend.pc = self.backend.memoryRead(1)
            return
        if 0 <= ea <= 5:
            self.backend.mfr |= 8
            self.backend.debugGuiPrint("Illegal Memory Address to Reserved Locations")
            self.backend.pc = self.backend.memoryRead(1)
            return
        self.backend.gpr[i.gprIndex] = self.backend.memoryRead(ea)
        string1 = "GPR: {0:d} EA: {1:X}".format(i.gprIndex, ea)
        self.backend.debugGuiPrint(string1)

    def str(self, i: Ins.Instruction):
        global backend
        self.backend.debugGuiPrint("Running STR")
        ea = self.computeEA(i)
        if ea > 2048:
            self.backend.mfr |= 8
            self.backend.debugGuiPrint("Illegal Memory Address beyond 2048")
            self.backend.pc = self.backend.memoryRead(1)
            return
        if 0 <= ea <= 5:
            self.backend.mfr |= 8
            self.backend.debugGuiPrint("Illegal Memory Address to Reserved Locations")
            self.backend.pc = self.backend.memoryRead(1)
            return
        self.backend.memoryWrite(ea, self.backend.gpr[i.gprIndex])
        string1 = "GPR: {0:d} EA: {1:X}".format(i.gprIndex, ea)
        self.backend.debugGuiPrint(string1)

    def lda(self, i: Ins.Instruction):
        global backend
        self.backend.debugGuiPrint("Running LDA")
        ea = self.computeEA(i)
        self.backend.gpr[i.gprIndex] = ea
        string1 = "GPR: {0:d} EA: {1:X}".format(i.gprIndex, ea)
        self.backend.debugGuiPrint(string1)

    def ldx(self,  i: Ins.Instruction):
        global backend
        self.backend.debugGuiPrint("Running LDX")
        ea = self.computeIXREA(i)

        if ea > 2048:
            self.backend.mfr |= 8
            self.backend.debugGuiPrint("Illegal Memory Address beyond 2048")
            self.backend.pc = self.backend.memoryRead(1)
            return
        if 0 <= ea <= 5:
            self.backend.mfr |= 8
            self.backend.debugGuiPrint("Illegal Memory Address to Reserved Locations")
            self.backend.pc = self.backend.memoryRead(1)
            return
        self.backend.ixr[i.ixrIndex] = self.backend.memoryRead(ea)
        string1 = "IXR: {0:d} EA: {1:X}".format(i.ixrIndex, ea)
        self.backend.debugGuiPrint(string1)

    def stx(self, i: Ins.Instruction):
        global backend
        ea = self.computeIXREA(i)
        if ea > 2048:
            self.backend.mfr |= 8
            self.backend.debugGuiPrint("Illegal Memory Address beyond 2048")
            self.backend.pc = self.backend.memoryRead(1)
            return
        if 0 <= ea <= 5:
            self.backend.mfr |= 8
            self.backend.debugGuiPrint("Illegal Memory Address to Reserved Locations")
            self.backend.pc = self.backend.memoryRead(1)
            return
        self.backend.memoryWrite(ea, self.backend.ixr[i.ixrIndex])
        string1 = "Running STX! IXR: {0:d} EA: {1:X}".format(i.ixrIndex, ea)
        self.backend.debugGuiPrint(string1)

    def jz(self, i: Ins.Instruction):
        global backend
        ea = self.computeEA(i)
        if self.backend.gpr[i.gprIndex] == 0:
            self.backend.pc = ea
            string1 = "Running JZ! GPR {0:d} is 0, jump to {1:X}".format(i.gprIndex, ea)
            self.backend.debugGuiPrint(string1)
            return
        string2 = "Running JZ! GPR {0:d} is not 0, not jump".format(i.gprIndex)
        self.backend.debugGuiPrint(string2)

    def jne(self, i: Ins.Instruction):
        global backend
        ea = self.computeEA(i)

        if self.backend.gpr[i.gprIndex] != 0:
            self.backend.pc = ea
            string1 = "Running JNE! GPR {0:d} is not 0, jump to {1:X}".format(i.gprIndex, ea)
            self.backend.debugGuiPrint(string1)
            return
        string2 = "Running JNE! GPR {0:d} is 0, not jump".format(i.gprIndex)
        self.backend.debugGuiPrint(string2)

    def jcc(self,i: Ins.Instruction):
        global backend
        ea = self.computeEA(i)
        bitMask = 0
        if i.gprIndex == 0:
            bitMask = 1
        elif i.gprIndex == 1:
            bitMask = 2
        elif i.gprIndex == 2:
            bitMask = 4
        elif i.gprIndex == 3:
            bitMask = 8
        if (self.backend.cc & bitMask) != 0:
            self.backend.pc = ea
            string1 = "Running JCC! CC {0:d} equals to required CC: {1:d} jump to {2:X}".format(self.backend.cc, i.gprIndex, ea)
            self.backend.debugGuiPrint(string1)
            return
        string2 = "Running JCC! CC {0:d} not equal to required CC: {1:d}".format(self.backend.cc, i.gprIndex)
        self.backend.debugGuiPrint(string2)

    def jma(self, i: Ins.Instruction):
        global backend
        ea = self.computeEA(i)
        self.backend.pc = ea
        string1 = "Running JMA! Jump to {0:X}".format(ea)
        self.backend.debugGuiPrint(string1)

    def jsr(self, i: Ins.Instruction):
        global backend
        ea = self.computeEA(i)
        self.backend.gpr[3] = self.backend.pc
        self.backend.pc = ea
        string1 = "Running JSR! Jump to {0:X}, current Args at{1:X}".format(ea, self.backend.gpr[0])
        self.backend.debugGuiPrint(string1)

    def jgt(self, i: Ins.Instruction):

        ea = self.computeIXREA(i)
        if self.backend.gpr[i.rx] > self.backend.gpr[i.ry]:
            self.backend.pc = ea
            string1 = "Running JGT! Jump to {0:X}".format(ea)
            self.backend.debugGuiPrint(string1)
            return
        string2 = "Running JGT! Not jump to {0:X}".format(ea)
        self.backend.debugGuiPrint(string2)

    def rfs(self, i: Ins.Instruction):

        self.backend.pc = self.backend.gpr[3]
        self.backend.gpr[0] = i.addr
        string1 = "Running RFS! Return to {0:X}, return value at {1:X}".format(self.backend.gpr[3], self.backend.gpr[0])
        self.backend.debugGuiPrint(string1)

    def sob(self, i: Ins.Instruction):
        global backend
        ea = self.computeEA(i)
        self.backend.gpr[i.gprIndex] -= 1
        if self.backend.gpr[i.gprIndex] < 0:
            self.backend.gpr[i.gprIndex] = int(math.pow(2, 16) - 1)
            self.backend.cc |= 2
            self.backend.debugGuiPrint("  Underflow!")
        if self.backend.gpr[i.gprIndex] > 0:
            self.backend.pc = ea
            string1 = "Running SOB! GPR{0:d}: {1:d}, jump to {2:X}".format(i.gprIndex, self.backend.gpr[i.gprIndex], ea)
            self.backend.debugGuiPrint(string1)
            return
        string2 = "Running SOB! GPR{0:d}: {1:d}, not jump".format(i.gprIndex, self.backend.gpr[i.gprIndex])
        self.backend.debugGuiPrint(string2)

    def jge(self, i: Ins.Instruction):
        global backend
        ea = self.computeEA(i)
        if self.backend.gpr[i.gprIndex] >= 0:
            self.backend.pc = ea
            string1 = "Running JGE! GPR{0:d}: {1:d}, jump to {2:X}".format(i.gprIndex, self.backend.gpr[i.gprIndex], ea)
            self.backend.debugGuiPrint(string1)
            return
        string2 = "Running JGE! GPR{0:d}: {1:d}, not jump".format(i.gprIndex, self.backend.gpr[i.gprIndex])
        self.backend.debugGuiPrint(string2)

    def amr(self, i: Ins.Instruction):
        global backend
        ea = self.computeEA(i)
        if ea > 2048:
            self.backend.mfr |= 8
            self.backend.debugGuiPrint("Illegal Memory Address beyond 2048")
            self.backend.pc = self.backend.memoryRead(1)
            return
        if 0 <= ea <= 5:
            self.backend.mfr |= 8
            self.backend.debugGuiPrint("Illegal Memory Address to Reserved Locations")
            self.backend.pc = self.backend.memoryRead(1)
            return
        self.backend.gpr[i.gprIndex] += self.backend.memoryRead(ea)
        if self.backend.gpr[i.gprIndex] > 65535:
            self.backend.gpr[i.gprIndex] -= 65536
            self.backend.cc |= 1
            self.backend.debugGuiPrint("  Overflow!")
        string1 = "Running AMR! Add {0:d} at {1:X} to GPR{2:d}, result is {3:d}".format(self.backend.memory.load(ea), ea, i.gprIndex, self.backend.gpr[i.gprIndex])
        self.backend.debugGuiPrint(string1)

    def smr(self, i: Ins.Instruction):
        global backend
        ea = self.computeEA(i)

        if ea > 2048:
            self.backend.mfr |= 8
            self.backend.debugGuiPrint("Illegal Memory Address beyond 2048")
            self.backend.pc = self.backend.memoryRead(1)
            return

        if 0 <= ea <= 5:
            self.backend.mfr |= 8
            self.backend.debugGuiPrint("Illegal Memory Address to Reserved Locations")
            self.backend.pc = self.backend.memoryRead(1)
            return
        self.backend.gpr[i.gprIndex] -= self.backend.memoryRead(ea)
        if self.backend.gpr[i.gprIndex] < 0:
            self.backend.gpr[i.gprIndex] += 65536
            self.backend.cc |= 2
            self.backend.debugGuiPrint("  Underflow!")
        string1 = "Running SMR! Sub {0:d} at {1:X} from GPR{2:d}, result is {3:d}".format(self.backend.memory.load(ea),
                                                                                          ea, i.gprIndex,
                                                                                          self.backend.gpr[i.gprIndex])
        self.backend.debugGuiPrint(string1)

    def air(self, i: Ins.Instruction):
        global backend
        ea = self.computeEA(i)
        self.backend.gpr[i.gprIndex] += ea
        if self.backend.gpr[i.gprIndex] > 65535:
            self.backend.gpr[i.gprIndex] -= 65536
            self.backend.cc |= 1
            self.backend.debugGuiPrint("  Overflow!")
        string1 = "Running AIR! Add {0:d} to GPR{1:d}, result is {2:d}".format(ea, i.gprIndex,
                                                                               self.backend.gpr[i.gprIndex])
        self.backend.debugGuiPrint(string1)

    def sir(self, i: Ins.Instruction):
        global backend
        ea = self.computeEA(i)
        self.backend.gpr[i.gprIndex] -= ea
        if self.backend.gpr[i.gprIndex] < 0:
            self.backend.gpr[i.gprIndex] += 65536
            self.backend.cc |= 2
            self.backend.debugGuiPrint("  Underflow!")
        string1 = "Running SIR! Sub {0:d} from GPR{1:d}, result is {2:d}".format(ea, i.gprIndex,
                                                                                 self.backend.gpr[i.gprIndex])
        self.backend.debugGuiPrint(string1)

    def mlt(self, i: Ins.Instruction):
        global backend
        result = self.backend.gpr[i.rx] * self.backend.gpr[i.ry]
        resultStr = "{0:32b}".format(result).replace(' ', '0')
        hBits = resultStr[0:16]
        lBits = resultStr[16:32]
        self.backend.gpr[i.rx] = int(hBits, base=2)
        self.backend.gpr[i.rx + 1] = int(lBits, base=2)
        string1 = "Running MLT! MLT r{0:d} with r{1:d}, result is {2:d} {3:s} {4:s} {5:s}".format(i.rx, i.ry, result,
                                                                                                  resultStr, hBits,
                                                                                                  lBits)
        self.backend.debugGuiPrint(string1)

    def dvd(self, i: Ins.Instruction):
        global backend
        if self.backend.gpr[i.ry] == 0:
            self.backend.debugGuiPrint("  Divide by 0")
            self.backend.cc |= 4
            return
        quotient = int(self.backend.gpr[i.rx] / self.backend.gpr[i.ry])
        remainder = self.backend.gpr[i.rx] % self.backend.gpr[i.ry]
        self.backend.gpr[i.rx] = quotient
        self.backend.gpr[i.rx + 1] = remainder
        string1 = "Running DVD! DVD r{0:d} with r{1:d}, quotient is {2:d} , remainder is {3:d}".format(i.rx, i.ry,
                                                                                                       quotient,
                                                                                                       remainder)
        self.backend.debugGuiPrint(string1)

    def trr(self, i: Ins.Instruction):
        global backend
        if self.backend.gpr[i.rx] == self.backend.gpr[i.ry]:
            self.backend.cc |= 8
            string1 = "Running TRR! r{0:d} equals to r{1:d}".format(i.rx, i.ry)
            self.backend.debugGuiPrint(string1)
            return
        string2 = "Running TRR! r{0:d} not equals to r{1:d}".format(i.rx, i.ry)
        self.backend.debugGuiPrint(string2)

    def andd(self, i: Ins.Instruction):
        global backend
        self.backend.gpr[i.rx] &= self.backend.gpr[i.ry]
        string1 = "Running AND! r{0:d} AND r{1:d}".format(i.rx, i.ry)
        self.backend.debugGuiPrint(string1)

    def orr(self, i: Ins.Instruction):
        global backend
        self.backend.gpr[i.rx] |= self.backend.gpr[i.ry]
        string1 = "Running ORR! r{0:d} ORR r{1:d}".format(i.rx, i.ry)
        self.backend.debugGuiPrint(string1)

    def nott(self, i: Ins.Instruction):
        global backend
        result = ~(self.backend.gpr[i.rx])
        resultStr = "{0:b}".format(result)
        resultStr = resultStr[len(resultStr) - 16:]

        self.backend.gpr[i.rx] = int(resultStr, base=2)
        string1 = "Running NOT! NOT r{0:d}".format(i.rx)
        self.backend.debugGuiPrint(string1)

    def src(self, i: Ins.Instruction):
        global backend
        origin = "{0:16b}".format(self.backend.gpr[i.gprIndex]).replace(' ', '0')
        result = ""
        if i.lr == 0:
            if '1' in origin[16 - i.count:]:
                self.backend.cc |= 2
                self.backend.debugGuiPrint("  Underflow!")
        else:
            print(origin[0:i.count])
            if '1' in origin[0:i.count]:
                self.backend.cc |= 1
                self.backend.debugGuiPrint("  Overflow!")
        if i.al == 1:
            if i.lr == 0:
                self.backend.debugGuiPrint("Shifting right")
                j = 0
                while j < i.count:
                    j += 1
                    result += '0'
                result += origin[0:16 - i.count]
            else:
                self.backend.debugGuiPrint("Shifting left")
                result += origin[i.count:]
                j = 0
                while j < i.count:
                    j += 1
                    result += '0'
        else:
            self.backend.debugGuiPrint("Shift arithmetically")
            maskBit = origin[0]

            if i.lr == 0:
                self.backend.debugGuiPrint("Shifting right")
                j = 0
                while j < i.count:
                    j += 1
                    result += maskBit
                result += origin[0:16 - i.count]

            else:
                self.backend.debugGuiPrint("Shifting left")
                result += origin[i.count:]
                j = 0
                while j < i.count:
                    j += 1
                    result += '0'
        self.backend.gpr[i.gprIndex] = int(result, base=2)
        string1 = "Running SRC! Prev binary: {}, result: {}".format(origin, result)
        backend.debugGuiPrint(string1)

    def rrc(self, i: Ins.Instruction):
        global backend
        origin = "{0:16b}".format(self.backend.gpr[i.gprIndex]).replace(' ', '0')
        if i.lr == 0:
            self.backend.debugGuiPrint("Rotating right")
            result = origin[16 - i.count:] + origin[0:16 - i.count]
        else:
            self.backend.debugGuiPrint("Rotating left")
            result = origin[i.count:] + origin[0:i.count]
        self.backend.gpr[i.gprIndex] = int(result, base=2)
        string1 = "Running RRC! Prev binary: {}, result: {}".format(origin, result)
        self.backend.debugGuiPrint(string1)

    def inn(self, i: Ins.Instruction):
        global backend
        devID = self.computeEA(i)
        if devID == 0:
            c = self.backend.iogui.popconsole()
            self.backend.gpr[i.gprIndex] = ord(c)
            string1 = "Running IN! Read {0} from keyboard, store to gpr{1:d}".format(c, i.gprIndex)
            self.backend.debugGuiPrint(string1)
        elif devID == 2:
            c = self.backend.iogui.popCR()
            self.backend.gpr[i.gprIndex] = ord(c)
            string1 = "Running IN! Read {0} from card reader, store to gpr{1:d}".format(c, i.gprIndex)
            self.backend.debugGuiPrint(string1)
        else:
            self.backend.debugGuiPrint("  Invalid operands")

    def out(self, i: Ins.Instruction):
        global backend
        devID = i.addr

        if devID != 1:
            self.backend.debugGuiPrint("  Invalid operands")
            return
        if i.indirect == 1:
            self.backend.iogui.insertPrint(chr(self.backend.gpr[i.gprIndex]))
        else:
            self.backend.iogui.pushPrint(chr(self.backend.gpr[i.gprIndex]))
        string1 = "Running OUT! Print {} to console printer".format(chr(self.backend.gpr[i.gprIndex]))
        self.backend.debugGuiPrint(string1)

    def trap(self, i : Ins.Instruction):
        self.backend.memoryWrite(2, self.backend.pc + 1)
        self.backend.pc = self.backend.memoryRead(self.backend.memoryRead(0) + i.trapcode)
        self.backend.debugGuiPrint("Running Trap")

    def chk(self, i : Ins.Instruction):
        devID = self.computeEA(i)
        if devID == 0:
            if (self.backend.iogui.isconsoleEmpty()):
                self.backend.gpr[i.gprIndex] = 0
                self.backend.debugGuiPrint("No console input to read")
            else:
                self.backend.gpr[i.gprIndex] = 1
                self.backend.debugGuiPrint("console input can read")
        elif devID == 1:
            self.backend.gpr[i.gprIndex] = 1
            self.backend.debugGuiPrint("console print is enabled")
        elif devID == 2:
            if (self.backend.iogui.isCREmpty()):
                self.backend.gpr[i.gprIndex] = 0
                self.backend.debugGuiPrint("No CR input to read")
            else:
                self.backend.gpr[i.gprIndex] = 1
                self.backend.debugGuiPrint("CR input can read")
        else:
            self.backend.gpr[i.gprIndex] = 0

    def fadd(self, i: Ins.Instruction):
        global backend
        devID = self.computeEA(i)
        fr_num = i.gprIndex
        # set IR

        FRDecimal = Floatrepresentation(self.backend.fr[fr_num])
        c_ea = self.backend.memory.load(devID)
        c_fr = FRDecimal.calculateDecimalNumber()
        floatFR = c_ea + c_fr

        res = Floatrepresentation(floatFR)
        self.backend.fr[fr_num] = res.tostring()
        string1 = "Running FADD! {0:d} plus {1:f} is stored in fr{2:d}, result is ".format(c_ea,
                                                                                                c_fr, fr_num)
        string1 += self.backend.fr[fr_num]

        self.backend.debugGuiPrint(string1)

    def fsub(self, i: Ins.Instruction):
        global backend
        devID = self.computeEA(i)
        fr_num = i.gprIndex
        # set IR

        FRDecimal = Floatrepresentation(self.backend.fr[fr_num])
        c_ea = self.backend.memory.load(devID)
        c_fr = FRDecimal.calculateDecimalNumber()
        floatFR = float(c_fr - c_ea)
        res = Floatrepresentation(floatFR)
        self.backend.fr[fr_num] = res.tostring()
        string1 = "Running FSUB! {0:f} minus {1:d} is stored in fr{2:d}, result is".format(c_fr,
                                                                                           c_ea, fr_num, )
        string1 += self.backend.fr[fr_num]
        self.backend.debugGuiPrint(string1)

    def vadd(self, i: Ins.Instruction):
        global backend
        ea_1 = self.computeEA(i)
        i.addr += 1
        ea_2 = self.computeEA(i)
        fr_num = i.gprIndex
        self.backend.debugGuiPrint("Running VADD")
        ea_v1 = self.backend.memory.load(ea_1)
        ea_v2 = self.backend.memory.load(ea_2)
        floatLength = Floatrepresentation(self.backend.fr[fr_num])
        vectorLength = int(floatLength.calculateDecimalNumber())
        for j in range(vectorLength):
            v1 = self.backend.memory.load(ea_v1 + j)
            v2 = self.backend.memory.load(ea_v2 + j)
            result = v1 + v2
            self.backend.memory.store(ea_v1, result)
            string1 = "{0:d} plus {1:d} is stored in {2:d}, result is {3:d}".format(v1, v2, ea_v1, result)
            self.backend.debugGuiPrint(string1)

    def vsub(self, i: Ins.Instruction):
        global backend
        ea_v1 = self.computeEA(i)
        i.addr += 1
        ea_v2 = self.computeEA(i)
        fr_num = i.gprIndex
        self.backend.debugGuiPrint("Running VSUB")
        floatLength = Floatrepresentation(self.backend.fr[fr_num])
        vectorLength = int(floatLength.calculateDecimalNumber())
        for j in range(vectorLength):
            v1 = self.backend.memory.load(ea_v1 + j)
            v2 = self.backend.memory.load(ea_v2 + j)
            result = v1 - v2
            self.backend.memory.store(ea_v1, result)
            string1 = "{0:d} minus {1:d} is stored in {2:d}, result is {3:d}".format(v1, v2, ea_v1, result)
            self.backend.debugGuiPrint(string1)

    def ldfr(self, i: Ins.Instruction):
        global backend
        devID = self.computeEA(i)
        fr_num = i.gprIndex
        # exp = "0000000"
        # man = "00000000"
        # expI = self.backend.memory.load(devID)
        # manI = self.backend.memory.load(devID + 1)
        # temp = "{0:b}".format(expI)
        # exp = exp[0:7 - len(temp)] + temp
        # temp1 = "{0:b}".format(manI)
        # man = temp1 + man[len(temp1):]
        # frs = exp + man
        # result = int(frs, base=2)
        # self.backend.fr[fr_num] = result
        # string1 = "Running LDFR! fr{0:d} : ".format(fr_num)
        # string1 += frs
        # self.backend.debugGuiPrint(string1)
        self.backend.fr[fr_num] = "{0:16b}".format(self.backend.memory.load(devID)).replace(' ', '0')
        string1 = "Running LDFR! fr{0:d} : ".format(fr_num)
        string1 += self.backend.fr[fr_num]
        self.backend.debugGuiPrint(string1)

    def stfr(self, i: Ins.Instruction):
        global backend
        devID = self.computeEA(i)
        fr_num = i.gprIndex
        # c_fr = self.backend.fr[fr_num]
        # c_fr = "{0:16b}".format(c_fr).replace(' ', '0')
        # man = int(c_fr[8:16], base=2)
        # exp = int(c_fr[0:8], base=2)
        # self.backend.memory.store(devID, exp)
        # self.backend.memory.store(devID + 1, man)
        # string1 = "Running STFR! (devID, exp) : ({0:d},{1:d}), (devID + 1, man) : ({2:d},{3:d})".format(devID, exp, devID + 1, man)
        # self.backend.debugGuiPrint(string1)
        self.backend.memory.store(devID, int(self.backend.fr[fr_num], base=2))
        string1 = "Running STFR!"
        self.backend.debugGuiPrint(string1)

    def cnvrt(self, i: Ins.Instruction):
        global backend
        devID = self.computeEA(i)
        fr_num = i.gprIndex
        self.backend.debugGuiPrint("Running CNVRT")
        f = self.backend.gpr[i.gprIndex]
        if f == 0:
            self.backend.gpr[i.gprIndex] = round(self.backend.memory.load(devID))
        elif f == 1:
            memoryNumber = self.backend.memory.load(devID)
            floatNumber = Floatrepresentation(float(memoryNumber))
            res = int(floatNumber.tostring(), base=2)
            self.backend.gpr[i.gprIndex] = res

        # if fr_num == 0:
        #     self.backend.gpr[i.gprIndex] = round(self.backend.memory.load(devID))
        # if fr_num == 1:
        #     exp = "0000000"
        #     man = "00000000"
        #     input = ""
        #     output = ""
        #     if self.backend.memory.load(devID) >= 0:
        #         input = "{0:b}".format(self.backend.memory.load(devID))
        #         man = input + man[len(input):]
        #         tmp = "{0:b}".format(len(input))
        #         exp = exp[0:7 - len(tmp)] + tmp
        #         output = '0' + exp + man
        #     else:
        #         fr = -1 * self.backend.memory.load(devID)
        #         input = "{0:b}".format(fr)
        #         for i in range(len(input)):
        #             if input[i] == '0':
        #                 input = input[0,i] + '1' + input[i+1:len(input)]
        #             else:
        #                 input = input[0, i] + '0' + input[i + 1:len(input)]
        #         i = len(input) - 1
        #         while i >= 0:
        #             if input[i] == '0':
        #                 input = input[0,i] + '1' + input[i+1:len(input)]
        #                 break
        #             else:
        #                 input = input[0, i] + '0' + input[i + 1:len(input)]
        #                 i -= 1
        #                 continue
        #
        #         man = input + man[len(input):]
        #         tmp = "{0:b}".format(len(input))
        #         exp = exp[0:7 - len(tmp)] + tmp
        #         output = "1" + exp + man
        #     self.backend.fr[0] = int(output, base=2)

class Floatrepresentation:
    global s
    global exponent
    global mantissa
    def __init__(self, number):
        global s
        global exponent
        global mantissa
        if isinstance(number, str):
            self.s = number[0:1]
            self.exponent = number[1:8]
            self.mantissa = number[8:]
        elif isinstance(number, float):
            k = struct.pack('>f', number)
            binaryint = struct.unpack('>l', k)[0]
            binary = "{0:32b}".format(binaryint).replace(' ', '0')
            self.s = binary[0] + ""
            exp = binary[1:9]
            self.exponent = self.evaluateEXP(exp)
            self.mantissa = binary[9:17]

    def tostring(self):
        global s
        global exponent
        global mantissa
        return self.s + self.exponent + self.mantissa

    def calculateDecimalNumber(self):
        global s
        global exponent
        global mantissa
        if self.s[0] == "0":
            sign = 1
        else:
            sign = -1
        valueexponent = pow(2, float(self.calculateExponent()))
        return sign * (self.calculateMantissa() * float(valueexponent))

    def calculateExponent(self):
        global s
        global exponent
        global mantissa
        if self.exponent[0] == "0":
            sign = 1
        else:
            sign = -1
        num = int(self.exponent[1:], base=2)
        if sign > 0:
            num += 1
        return sign * num

    def calculateMantissa(self):
        global s
        global exponent
        global mantissa
        a = float(1/2)
        b = float(1/4)
        c = float(1/8)
        d = float(1/16)
        e = float(1/32)
        f = float(1/64)
        g = float(1/128)
        h = float(1/256)
        mantissavec = [a, b, c, d, e, f, g, h]
        mantissaFraction = float(0)
        i = 0
        while i < 8:
            bit = self.mantissa[i]
            if bit == "1":
                mantissaFraction += mantissavec[i]
            i += 1
        return 1 + mantissaFraction

    def evaluateEXP(self, exp):
        num = int(exp, base=2)
        num -= 127
        if num > 64:
            return ""
        if num < -63:
            return ""
        if num <= 0:
            expart1 = "1"
        else:
            expart1 = "0"
        if num > 0:
            num -= 1
        if num < 0:
            num *= -1

        return expart1 + "{0:6b}".format(num).replace(' ', '0')

    def sets(self, s):
        self.s = s

    def setexp(self, exponent):
        self.exponent = exponent

    def setman(self, mantissa):
        self.mantissa = mantissa










