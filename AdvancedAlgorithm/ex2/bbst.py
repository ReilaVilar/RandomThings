from math import floor

class Node:
    def __init__(self, data): 
        self.data = data
        self.left = self.right = None

def init_bbst(list):
    m = len(list)

    if not list:
        return

    mid_element = floor(m/2)
    root = Node(list[mid_element])

    left_list = list[:mid_element]
    right_list = list[mid_element+1:]  # also exclude the root

    root.left = init_bbst(left_list)
    
    root.right = init_bbst(right_list)

    return root

def Binary_search(text, root):
    count = 0
    for word in text:
        rt = root
        match = False
        while not match:
            if word == rt.data:
                match = True
            elif word < rt.data:
                if rt.left != None:
                    rt = rt.left
                    continue
            elif word > rt.data:
                if rt.right != None:
                    rt = rt.right
                    continue
            break
        if not match:
            count+=1
    return count


def Insertion_sort(list):
    for i in range(1, len(list)+1, 1):
        for j in range(i-1, 0, -1):
            if list[j-1] > list[j]:
                temp = list[j-1]
                list[j-1] = list[j]
                list[j] = temp
            else:
                break
    return list