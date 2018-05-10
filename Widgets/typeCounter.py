class typeCounter(dict):
    def __init__(self, sub={}):
        super(typeCounter, self).__init__()
        self.sub = sub

    def counter(self, type):
        if type not in self:
            return 1
        return self[type] + 1

    def value(self, type):
        if type not in self:
            return 1
        return self[type]

    def add(self, type, n=1):
        type = self.sub[type] if type in self.sub else type
        if type not in self:
            self[type] = n
        else:
            self[type] += n
        return self[type]

    def subtract(self, type):
        type = self.sub[type] if type in self.sub else type
        if type not in self:
            self[type] = 0
        else:
            self[type] = self[type] - 1 if self[type] > 0 else 0
        return self[type]
