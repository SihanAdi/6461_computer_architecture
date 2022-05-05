import Underlyinglogic


class Cache:


    addrList = []
    contentList = []

    def __init__(self, max_v, backEnd : Underlyinglogic):

        global backend
        global max_value
        self.backend = backEnd
        self.max_value = max_v

    def read(self, addr):
        global addrList
        global contentList

        if addr in self.addrList:
            pos = self.addrList.index(addr)
        else:
            return -1
        content = self.contentList[pos]
        self.addrList.pop(pos)
        self.contentList.pop(pos)
        self.addrList.append(addr)
        self.contentList.append(content)
        return content

    def write(self, addr, content):
        global addrList
        global contentList
        if addr in self.addrList:
            pos = self.addrList.index(addr)
            precontent = self.contentList[pos]
            if precontent != content:
                self.addrList.pop(pos)
                self.contentList.pop(pos)
                self.addrList.append(addr)
                self.contentList.append(content)
            return
        if len(self.addrList) >= self.max_value:
            self.backend.memory.store(self.addrList.pop(0), self.contentList.pop(0))
            self.backend.simulateDelay()
        self.addrList.append(addr)
        self.contentList.append(content)

    def flush(self):
        global addrList
        global contentList
        for index in range(len(self.addrList)):
            self.backend.memory.store(self.addrList[index], self.contentList[index])
        self.addrList = []
        self.contentList = []








