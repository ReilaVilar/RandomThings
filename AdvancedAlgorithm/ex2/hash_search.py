class Hashmap:
    def __init__(self):
        self.size = 256
        self.map = [None] * self.size
    
    def _get_hash(self, key):
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size
    
    def add(self, key):
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            self.map[key_hash] = [key]
            return True
        else:
            self.map[key_hash].append(key)
            return True

def init_hashmap(list):
    h = Hashmap()
    for element in list:
        h.add(element)
    return h

def Hash_search(text, map):
    count = 0
    for word in text:
        word_hash = 0
        for i in word:
            word_hash += ord(i)
        word_hash %= map.size
        if map.map[word_hash] != None:
            if word not in map.map[word_hash]:
                count += 1
        else:
            count += 1
    return count
