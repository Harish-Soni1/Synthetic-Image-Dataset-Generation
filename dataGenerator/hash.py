class HashTable:

    def __init__(self):
        self.max = 10
        self.arr = [[] for i in range(self.max)]

    def get_hash(self, key):
        h = 0
        for ch in key:
            h += ord(ch)

        return h % self.max

    def __setitem__(self, key, value):
        h = self.get_hash(key)
        found = False

        for ind, element in enumerate(self.arr[h]):
            if len(element) == 2 and element[0] == key:
                found = True
                if self.arr[h][ind][1] < 30:
                    self.arr[h][ind][1] += value
                    break

        if not found:
            self.arr[h].append([key, value])

    def __getitem__(self, key):
        h = self.get_hash(key)
        values = [0]
        ind = 0
        for inx, element in enumerate(self.arr[h]):
            if len(element) == 2 and element[0] == key:
                values.append(element[1])
                ind += 1

        return values[ind]


