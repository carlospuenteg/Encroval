def enc(txt,encryption):
    encTxt = ""
    for x in txt:
        encTxt += encryption[int(x,16)]  # The symbol in the equivalent position
    return encTxt

def dec(txt,encryption):
    hexa = "0123456789abcdef"
    decTxt = ""
    for x in txt:
        decTxt += hexa[encryption.index(x)]  # The symbol in the equivalent position
    return decTxt