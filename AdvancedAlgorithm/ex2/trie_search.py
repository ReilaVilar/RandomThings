class Node:
    def __init__(self):
        self.children = [None]*26
        self.isEndOfWord = False
    
def charToIndex(char):
    return ord(char) - ord('a')

def init_trie(list):

    root = Node()

    for word in list:
        n = len(word)
        tempRoot = root

        for i in range(0, n):
            index = charToIndex(word[i]) 
            if tempRoot.children[index] == None:
                tempRoot.children[index] = Node()
            if i == n-1:
                tempRoot.children[index].isEndOfWord = True
                break
            tempRoot = tempRoot.children[index] 
    
    return root

def Trie_search(text, root):
    count = 0

    for word in text:
        rt = root
        j = 0
        for char in word:
            i = charToIndex(char)
            if i < 0 or i > 25:
                count+=1
                break
            if rt.children[i] == None:
                count+=1
                break
            if rt.children[i].isEndOfWord and j == len(word)-1:
                break  #match
            if not rt.children[i].isEndOfWord and j == len(word)-1:
                count+=1
                break
            rt = rt.children[i]
            j+=1
    return count
