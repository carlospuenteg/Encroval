import random
import hashlib
from colorama import init, Fore, Back
init(autoreset=True)
#-----------------------------------------------------------------------------
# https://www.geeksforgeeks.org/python-import-module-from-different-directory/
#-----------------------------------------------------------------------------
from hash2h import h2h
from txtHex import t2h, h2t, txtB
from enc1 import enc, dec

##################################################################################################################################

# https://newbedev.com/build-python-script-to-executable-file-for-windows-mac-os-linux
# pyinstaller --onefile test.py

#-----------------------------------------------------------------------------

symb = "0123456789abcdef"
maxLen = 94
textMLen = 126

##################################################################################################################################

def encrypt(txt,pwd):
    if not all(c in txtB for c in txt) or len(txt)>maxLen:
        return -1
    encList = [None] * 256
    #-----------------------------------------------------------------------------------------------------------------------------
    hashword = hashlib.sha512(pwd.encode()).hexdigest()

    iters = 100
    while True:
        hashword = h2h(hashword,iters)+h2h(hashword,iters+1)+h2h(hashword,iters+2)
        hashwLi = [int(hashword[i:i+2],16) for i in range(0, len(hashword), 2)]
        hashwLi = list(dict.fromkeys(hashwLi))
        if len(hashwLi)>=(textMLen+2):
            break
        iters += 10
    #-----------------------------------------------------------------------------------------------------------------------------
    encryption = ""

    iters = 200
    hashword = h2h(hashword,iters)+h2h(hashword,iters+1)+h2h(hashword,iters+2)
    while len(encryption)<16:
        if (hashword[hashwLi[50]] not in encryption):
            encryption += hashword[hashwLi[50]]
        else: 
            iters += 10
            hashword = h2h(hashword,iters)+h2h(hashword,iters+1)+h2h(hashword,iters+2)
    #-----------------------------------------------------------------------------------------------------------------------------
    txtEnc = enc(t2h(txt),encryption)
    txtPos = hashwLi[:textMLen]

    txtLen = len(txtEnc)
    txtLenEnc = enc(format(txtLen, 'x').rjust(2,"0"),encryption)
    txtLenPos = hashwLi[textMLen:textMLen+2]
    #-----------------------------------------------------------------------------------------------------------------------------
    for x in range(0,256):
        encList[x] = random.choice(symb)
    for x in range(0,len(txtEnc)):
        encList[txtPos[x]] = txtEnc[x]
    for x in range(0,len(txtLenPos)):
        encList[txtLenPos[x]] = txtLenEnc[x]

    encText = "".join(encList)
    if (decrypt(encText,pwd) == txt):
        return encText
    else:
        return -1

##################################################################################################################################

def decrypt(txt,pwd):
    if not all(c in symb for c in txt) or len(txt)>257:
        return -1
    #-----------------------------------------------------------------------------------------------------------------------------
    hashword = hashlib.sha512(pwd.encode()).hexdigest()

    iters = 100
    while True:
        hashword = h2h(hashword,iters)+h2h(hashword,iters+1)+h2h(hashword,iters+2)
        hashwLi = [int(hashword[i:i+2],16) for i in range(0, len(hashword), 2)]
        hashwLi = list(dict.fromkeys(hashwLi))
        if len(hashwLi)>=(textMLen+2):
            break
        iters += 10
    #-----------------------------------------------------------------------------------------------------------------------------
    encryption = ""

    iters = 200
    hashword = h2h(hashword,iters)+h2h(hashword,iters+1)+h2h(hashword,iters+2)
    while len(encryption)<16:
        if (hashword[hashwLi[50]] not in encryption):
            encryption += hashword[hashwLi[50]]
        else: 
            iters += 10
            hashword = h2h(hashword,iters)+h2h(hashword,iters+1)+h2h(hashword,iters+2)
    #-----------------------------------------------------------------------------------------------------------------------------
    txtPos = hashwLi[:textMLen]
    txtLenPos = hashwLi[textMLen:textMLen+2]
    txtLen = int(dec(txt[txtLenPos[0]]+txt[txtLenPos[1]],encryption),16)
    fiText = ""
    for x in range(0,txtLen):
        fiText += txt[txtPos[x]]
    fiText = h2t(dec(fiText,encryption))

    return fiText

##################################################################################################################################

def menu():
    print("\nThis algorithm helps you encrypt a text with a maximum length of " + str(maxLen) + ", written with 40 different characters and symbols")

    while True:
        print("  0. EXIT: ")
        print("  1. Encrypt a text")
        print("  2. Decrypt a text")
        print("  s. Symbols list")
        opt = input("\nType an option: ")

        if opt == "0":
            return 0
        elif opt == "1":
            txt = input("Type the text to encrypt: ")
            pwd = input("Type a password: ")
            encText = encrypt(txt,pwd)
            if encText != -1:
                print("\nEncrypted text: " + Fore.GREEN+encText+"\n")
            else:
                print("\n"+Fore.RED+"Invalid text"+"\n")
        elif opt == "2":
            txt = input("Type the text to decrypt: ")
            pwd = input("Type the password: ")
            decText = decrypt(txt,pwd)
            if decText != -1:
                print("\nDecrypted text: " + Fore.LIGHTCYAN_EX+decText+"\n")
            else:
                print("\n"+Fore.RED+"Invalid text"+"\n")
        elif opt == "s":
            baseList = ""
            for x in txtB:
                baseList += Back.BLUE+" "+x+" "
                baseList += Back.RESET+" "
            print("\n"+baseList+"\n")

##################################################################################################################################

menu()
