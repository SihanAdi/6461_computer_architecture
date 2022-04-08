class Memory:
    mem = []

    def __init__(self, size):
        self.size = size
        self.mem = [0] * self.size

    def load(self, key):
        global mem
        if key < self.size:
            self.value = self.mem[key]
            return self.value
        else:
            return False

    def store(self, key, value):
        global mem
        if len(self.mem) > self.size:
            return False
        if key < len(self.mem):
            self.mem[key] = value


