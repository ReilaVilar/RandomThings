from timeit import Timer
from bbst import Binary_search, Insertion_sort, init_bbst
from naive_search import Naive_search
from hash_search import Hash_search, init_hashmap
from trie_search import Trie_search, init_trie

M = 109584
DICT = [""]*M
TEXT = []

def properText(input):
    for i in range(len(input)):
        line = input[i]
        line = line.lower()
        for letter in line:
            if not letter.isalpha() and letter != " ":
                line = line.replace(letter, "")
        input[i] = line
    new_list = []
    for line in input:
        words = line.split(' ')
        for word in words:
            new_list.append(word)
    return new_list


if __name__=='__main__':
    spelling = 0

    print("_____________________________")
    print("Reading Files...")
    file_words = open("english_words.txt", "r", encoding="utf8")
    if file_words.mode == 'r':
        DICT = file_words.read().splitlines()

    file_text = open("Texts/100kb.txt", "r", encoding="utf8")
    if file_text.mode == 'r':
        TEXT = file_text.read().splitlines()
    TEXT = properText(TEXT)
    

    print("_____________________________")
    print("Precomputations...")
    hashmap = init_hashmap(DICT)

    sorted_DICT = Insertion_sort(DICT)
    binary_root = init_bbst(sorted_DICT)

    trie_root = init_trie(DICT)


    print("_____________________________")
    print("Initializing Speed:")
    hash_t = Timer(stmt="init_hashmap(DICT)", setup="from __main__ import DICT; from hash_search import init_hashmap")
    print("Hashmap:", hash_t.timeit(number=1))
    bbst_t = Timer(stmt="init_bbst(sorted_DICT)", setup="from __main__ import sorted_DICT; from bbst import init_bbst")
    print("Binary tree:", bbst_t.timeit(number=1))
    trie_t = Timer(stmt="init_trie(DICT)", setup="from __main__ import DICT; from trie_search import init_trie")
    print("Trie tree:", trie_t.timeit(number=1))
    

    print("_____________________________")
    print("Searching Speed:")
    hash_t = Timer(stmt="Hash_search(TEXT, hashmap)", setup="from __main__ import TEXT, hashmap; from hash_search import Hash_search")
    print("Hash:", hash_t.timeit(number=1))
    bbst_t = Timer(stmt="Binary_search(TEXT, binary_root)", setup="from __main__ import TEXT, binary_root; from bbst import Binary_search")
    print("BBST:", bbst_t.timeit(number=1))
    trie_t = Timer(stmt="Trie_search(TEXT, trie_root)", setup="from __main__ import TEXT, trie_root; from trie_search import Trie_search")
    print("Trie:", trie_t.timeit(number=1))
    
    #########  WARNING - This codeblock takes approximately 5:45 minutes  ###########
    # naive_t = Timer(stmt="Naive_search(TEXT, DICT, M)", setup="from __main__ import TEXT, DICT, M; from naive_search import Naive_search")
    # print("Naive:", naive_t.timeit(number=1))
    ################################################################################


    print("_____________________________")
    print("Results:")
    spelling = Hash_search(TEXT, hashmap)
    print("Hash:", spelling)
    spelling = Binary_search(TEXT, binary_root)
    print("BBST:", spelling)
    spelling = Trie_search(TEXT, trie_root)
    print("Trie:", spelling)
    
    #########  WARNING - This codeblock takes approximately 5:45 minutes  ###########
    # spelling = Naive_search(TEXT, DICT, M)
    # print("Naive:",spelling)
    ################################################################################
