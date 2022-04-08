class Instruction:
    def __init__(self, content):
        self.binaryStr = "{0:16b}".format(content).replace(' ', '0')
        self.opcode = int(self.binaryStr[0:6], base=2)
        self.gprIndex = int(self.binaryStr[6:8], base=2)
        self.ixrIndex = int(self.binaryStr[8:10], base=2) - 1
        self.indirect = int(self.binaryStr[10:11], base=2)
        self.addr = int(self.binaryStr[11:], base=2)
        self.rx = self.gprIndex
        self.ry = self.ixrIndex + 1
        self.al = int(self.binaryStr[8:9], base=2)
        self.lr = int(self.binaryStr[9:10], base=2)
        self.count = int(self.binaryStr[11:], base=2)
        self.trapcode = int(self.binaryStr[12:], base=2)
