def Naive_search(text, dict, size):
    count = 0
    for word in text:
        for i in range(size):
            if word == dict[i]:
                break
            if i == size-1:
                count += 1
    return count
