from timeit import Timer

def brute_force(haystack, needle):
    count = 0
    for i in range(len(haystack) - len(needle) + 1):
        match = True
        for j in range(len(needle)):
            if haystack[i+j] != needle[j]:
                match = False
                break
        if match:
            count += 1  # position: i

def KMP(haystack, needle):
    j = 0
    k = 0
    table = kmp_table(needle)
    count = 0

    while j<len(haystack):
        if needle[k] == haystack[j]:
            j = j + 1
            k = k + 1
            if k == len(needle):
                # return m <- j-k    # if only first occurance is needed
                count += 1  # position: j - k
                k = table[k]  # T[len(needle)] cant be -1
        else:
            k = table[k]
            if k < 0:
                j = j + 1
                k = k + 1
def kmp_table(needle):
    table = []
    table.append(-1)
    pos = 1   # current position in table
    cnd = 0   # zero based index in needle of the next char of the current candidate substring
    while pos < len(needle):
        if needle[pos] == needle[cnd]:
            table.append(table[cnd])
        else:
            table.append(cnd)
            while cnd >= 0 and needle[pos] != needle[cnd]:
                cnd = table[cnd]
        pos += 1
        cnd += 1
    table.append(cnd)

    return table



def sunday(haystack, needle):
    m = len(haystack)
    n = len(needle)
    i = 0
    count = 0
    while i < m-n:
        flag = 0
        shift = n
        for j in range(0, n):
            if haystack[i+j] != needle[j]:
                flag = -1
                break
        if flag == 0:
            count += 1
        p = needle.rfind(haystack[i+shift])
        if p == -1:
            shift = n + 1
        else:
            shift = n - p
        i = i + shift




NO_OF_CHARS = 256
def FSM(T, P):
    n = len(P)
    m = len(T)
    TF = [[0 for i in range(NO_OF_CHARS)] for j in range(n + 1)]
    TransitionFunction(P, n, TF)
    count = 0

    state = 0
    for i in range(m):
        state = TF[state][ord(T[i])]
        if state == n:
            count += 1   # position: i-n+1
def TransitionFunction(P, n, TF):
    lps = 0
    for x in range(NO_OF_CHARS):
        TF[0][x] = 0
    TF[0][ord(P[0])] = 1

    for i in range(1, n+1):
        for x in range(NO_OF_CHARS):
            TF[i][x] = TF[lps][x]
        if (i < n):
            TF[i][ord(P[i])] = i + 1
            lps = TF[lps][ord(P[i])]


def Rabin_Karp(T, P, prime):
    m = len(T)
    n = len(P)
    p = 0  # hash of pattern
    t = 0  # hash of text
    h = 1
    i = 0
    j = 0
    count = 0
    # h = pow(d, n-1)%prime
    for i in range(n-1):
        h = (h*NO_OF_CHARS) % prime

    for i in range(n):
        p = (NO_OF_CHARS*p + ord(P[i]))%prime
        t = (NO_OF_CHARS*t + ord(T[i]))%prime

    for i in range(m-n+1):
        if p == t:
            for j in range(n):
                if T[i+j] != P[j]:
                    break
                else:
                    j += 1
            if j == n:
                count += 1  # position: i
        if i < m-n:
            t = (NO_OF_CHARS*(t-ord(T[i])*h) + ord(T[i+n]))%prime
            if t < 0:
                t += prime

# the_prime number for rabin-karp
def prime(needle):
    primes = []
    the_prime = 2
    file = open("prime_numbers.txt", "r", encoding="utf8")
    primes_as_text=""
    if file.mode == 'r':
        primes_as_text = file.read()
    file.close()
    primes = primes_as_text.split(',')
    for i in range(len(primes)):
        if len(needle) < int(primes[i]):
            return int(primes[i])

def compare(haystack, needle):
    t = Timer(stmt="brute_force(haystack, needle)", setup="from __main__ import brute_force, haystack, needle")
    t2 = Timer(stmt="KMP(haystack, needle)", setup="from __main__ import KMP, haystack, needle")
    t3 = Timer(stmt="sunday(haystack, needle)", setup="from __main__ import sunday, haystack, needle")
    t4 = Timer(stmt="FSM(haystack, needle)", setup="from __main__ import FSM, haystack, needle")
    t5 = Timer(stmt="Rabin_Karp(haystack, needle, the_prime)", setup="from __main__ import Rabin_Karp, haystack, needle, the_prime")

    print ("Brute Force: ", t.timeit(number=10))
    print ("KMP: ", t2.timeit(number=10))
    print ("Sunday: ", t3.timeit(number=10))
    print ("FSM: ", t4.timeit(number=10))
    print ("Rabin-Karp: " ,t5.timeit(number=10))


if __name__=='__main__':
    needle = ""
    haystack = ""
    the_prime =  prime(needle)
    pat_list = ["10byte", "100byte", "1000byte", "10kb"]

    file = open( "Texts/100kb.txt", "r", encoding="utf8")
    if file.mode == 'r':
        haystack = file.read()
    file.close()

    for size in pat_list:
        file = open( "Patterns/P_" + size + ".txt", "r", encoding="utf8")
        if file.mode == 'r':
            needle = file.read()
        file.close()
        print ("\nPattern Length: " , size)
        compare(haystack, needle)


    txt_list = ["100byte", "10kb", "50kb", "100kb"]

    file = open( "Patterns/P_10byte.txt", "r", encoding="utf8")
    if file.mode == 'r':
        needle = file.read()
    file.close()

    for size in txt_list:
        file = open( "Texts/" + size + ".txt", "r", encoding="utf8")
        if file.mode == 'r':
            haystack = file.read()
        file.close()
        print ("\nText Length: " , size)
        compare(haystack, needle)

    needle = ""
    haystack = ""
    for i in range(20):
        needle += "a"
    for i in range(100000):
        haystack += "a"
    print("\nText lenght: ", len(haystack), " times 'a'")
    print("Pattern lenght: ", len(needle), " times 'a'")
    compare(haystack, needle)
    needle = ""
    haystack = ""
    for i in range(20):
        needle += "a"
    for i in range(500000):
        haystack += "a"
    print("\nText lenght: ", len(haystack), " times 'a'")
    print("Pattern lenght: ", len(needle), " times 'a'")
    compare(haystack, needle)
