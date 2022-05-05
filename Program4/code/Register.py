import math

class Register:
    length
    content
    def __init__(self, size):
        global length
        global content
        self.length = size
        self.content = 0

    def load(self):
        return self.content

    def store(self, value):
        global content
        self.content = value

    def increment(self):
        # Check the content, reset to 0 when overflow
        if self.content < math.pow(2, self.size) - 1:
            self.content += 1
        else:
            self.content = 0