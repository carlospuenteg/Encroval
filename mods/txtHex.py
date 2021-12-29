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
        d.append(txtB[num % bLen])
        num //= bLen

    return "".join(d[::-1])