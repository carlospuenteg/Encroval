txtB = "0123456789abcdefghijklmnopqrstuvwxyz .,'"
bLen = len(txtB)
hexB = "0123456789abcdef"

##########################################################

def t2h(txt):
    num = 0
    for x in range(0,len(txt)):
        num += ( txtB.index(txt[x]) * bLen**(len(txt)-x-1) )

    return format(num, 'x')

def h2t(hex):
    num = 0
    for x in range(0,len(hex)):
        num += ( hexB.index(hex[x]) * 16**(len(hex)-x-1) )

    d = []
    while num:
        d.append(txtB[num % bLen])   # >(8%2 = 0 / 4%2 = 0 / 2%2 = 0 / 1%2 = 1 )      >(9%4 = 1 / 2%4 = 2)
        num //= bLen                      # >(n = 4 / 2 / 1)                               >(n = 4 / 0 )

    return "".join(d[::-1])

#print(t2h("this is a test"))