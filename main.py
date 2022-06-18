import random
import hashlib
from colorama import init, Fore, Back; init(autoreset=True)
from PIL import Image
import numpy as np
import random

############################################################################
BASE = "0123456789abcdefghijklmnopqrstuvwxyz .,'"; 
BASE_LEN = len(BASE)
HEX_SYMB = "0123456789abcdef"
HASH_ITERS = 100
ITERS_TOADD = 10
ENC_CODE_POS = 0
HEX_POS_LEN = 6
IMG_SIZE = int(np.sqrt((16**HEX_POS_LEN)//6))
ENC_LIST_LEN = (IMG_SIZE**2)*6
TEXT_LEN_POS = range(1, HEX_POS_LEN+1)
##########################################################################################################
# Create a new hash from a hash
def h2h(hash, iters):
    for _ in range(iters):
        hash = hashlib.sha512(hash.encode()).hexdigest()
    return hash

# Encrypt a text with an encryption code
def enc(txt,encryption_code):
    encTxt = ""
    for x in txt:
        encTxt += encryption_code[int(x,16)]  # The symbol in the equivalent position
    return encTxt

# Decrypt an encrypted text with an encryption code
def dec(txt,encryption):
    decTxt = ""
    for x in txt:
        decTxt += HEX_SYMB[encryption.index(x)]  # The symbol in the equivalent position
    return decTxt

# Convert from text to hexadecimal
def t2h(txt):
    num = 0
    for x in range(0,len(txt)):
        num += ( BASE.index(txt[x]) * BASE_LEN**(len(txt)-x-1) )

    return format(num, 'x')

# Convert hexadecimal to text
def h2t(hex):
    num = 0
    for x in range(0,len(hex)):
        num += ( HEX_SYMB.index(hex[x]) * 16**(len(hex)-x-1) )

    d = []
    while num:
        d.append(BASE[num % BASE_LEN])
        num //= BASE_LEN

    return "".join(d[::-1])

##########################################################################################################
def encrypt(txt, pwd):
    txt = txt.lower()

    # If, for example, ENC_LIST_LEN = 200, then the text on hexadecimal can have a length of up to 197 (200-3)
    if not all(c in BASE for c in txt) or len(t2h(txt)) > ENC_LIST_LEN-1-HEX_POS_LEN : return -1

    # Encode the password to sha512 and get the hash (length = 128)
    hash = hashlib.sha512(pwd.encode()).hexdigest()

    # Initial number of iterations for the hash
    iters = HASH_ITERS

    # Create a new hash from the old hash
    hash = h2h(hash, iters)
    
    # Add ITERS_TOADD to the iterations count
    iters += ITERS_TOADD

    # Create a list with the indexes where the symbols will be saved, created in random order using the hash as the random seed
    random.seed(int(hash,16))
    pwd_indexes = random.sample(range(ENC_LIST_LEN), ENC_LIST_LEN)

    # Create a new hash to use to obtain the symbols used in the encryption and their order
    hash = h2h(hash, iters)

    # Symbols used in the encryption and their order
    encryption_code = ""

    # While the encryption string doesn't have 16 symbols
    while len(encryption_code) < 16:
        # If the symbol of the encr_hash in the position contained in pwd_indexes[ENC_CODE_POS] is not in the encryption string, add it to the encryption code
        if (hash[ENC_CODE_POS] not in encryption_code):
            encryption_code += hash[ENC_CODE_POS]
        # Create a new hash
        iters += ITERS_TOADD
        hash = h2h(hash,iters)

    # Encrypt the text (converted to hexadecimal) with the encryption code
    txt_enc = enc(t2h(txt), encryption_code)

    # Indexes for each character in the encrypted text
    txt_indexes = pwd_indexes[TEXT_LEN_POS[-1]+1:]

    # Encrypt the length of the text (converted to hexadecimal - in string) and adding a 0 to the left if the length is less than HEX_POS_LEN (f -> 0f)
    txt_len_enc = enc(format(len(txt_enc), 'x').rjust(HEX_POS_LEN,"0"), encryption_code)

    # Save the two indexes where the text length will be saved
    txt_len_indexes = [pwd_indexes[TEXT_LEN_POS[i]] for i in range(HEX_POS_LEN)]

    # Fill the encrypted text with random characters
    toret = [random.choice(HEX_SYMB) for _ in range(ENC_LIST_LEN)]

    # Place each character in the encrypted text in its position from txt_indexes
    for x in range(len(txt_enc)):
        toret[txt_indexes[x]] = txt_enc[x]
        
    # Place the length of the text in the two indexes from txt_len_indexes
    for x in range(0,len(txt_len_indexes)):
        toret[txt_len_indexes[x]] = txt_len_enc[x]

    # Join the toret list
    toret = "".join(toret)

    # If the text can be decrypted with the same password, return the result.
    if (decrypt(toret, pwd) == txt):
        return toret
    # Else, something went wrong
    else:
        return -1

##########################################################################################################

def decrypt(txt,pwd):
    # The symbols must all be hexadecimal and the text must have a length of ENC_LIST_LEN
    if not all(c in HEX_SYMB for c in txt) or len(txt) != ENC_LIST_LEN : return -1

    # Encode the password to sha512 and get the hash (length = 128)
    hash = hashlib.sha512(pwd.encode()).hexdigest()

    # Initial number of iterations for the hash
    iters = HASH_ITERS

    # Create a new hash from the old hash
    hash = h2h(hash, iters)
    
    # Add ITERS_TOADD to the iterations count
    iters += ITERS_TOADD

    # Create a list with the indexes where the symbols will be saved, created in random order using the hash as the random seed
    random.seed(int(hash,16))
    pwd_indexes = random.sample(range(ENC_LIST_LEN), ENC_LIST_LEN)

    # Create a new hash to use to obtain the symbols used in the encryption and their order
    hash = h2h(hash, iters)

    # Symbols used in the encryption and their order
    encryption_code = ""

    # While the encryption string doesn't have 16 symbols
    while len(encryption_code) < 16:
        # If the symbol of the encr_hash in the position contained in pwd_indexes[ENC_CODE_POS] is not in the encryption string, add it to the encryption code
        if (hash[ENC_CODE_POS] not in encryption_code):
            encryption_code += hash[ENC_CODE_POS]
        # Create a new hash
        iters += ITERS_TOADD
        hash = h2h(hash,iters)

    # Indexes for each character in the encrypted text
    txt_indexes = pwd_indexes[TEXT_LEN_POS[-1]+1:]

    # Save the two indexes where the text length will be saved
    txt_len_indexes = [pwd_indexes[TEXT_LEN_POS[i]] for i in range(HEX_POS_LEN)]

    # Get the text length from the text in the txt_len_indexes, decrypt it and convert it to integer
    txt_len = [txt[txt_len_indexes[i]] for i in range(HEX_POS_LEN)]
    txt_len = int(dec(''.join(txt_len), encryption_code), 16)

    toret = ""
    for x in range(txt_len):
        toret += txt[txt_indexes[x]]
    toret = h2t(dec(toret, encryption_code))

    return toret

##########################################################################################################
def encrypt_toimg(txt, pwd, img_path="img.png"):
    enc_text = encrypt(txt, pwd)
    img_arr = np.array([[int(enc_text[i:i+2], 16), int(enc_text[i+2:i+4], 16), int(enc_text[i+4:i+6], 16)] for i in range(0, len(enc_text), 6)], dtype=np.uint8)
    img_arr = img_arr.reshape(IMG_SIZE, IMG_SIZE, 3)
    Image.fromarray(img_arr).save(img_path)
    return enc_text

def decrypt_img(img_path, pwd):
    img_arr = np.array(Image.open(img_path)).flatten()
    img_str = "".join([f'{n:02x}' for n in img_arr])
    return decrypt(img_str, pwd)

##########################################################################################################
def menu():
    print("\nThis algorithm helps you encrypt a text with a maximum length of " + str(ENC_LIST_LEN) + ", written with 40 different characters and symbols")

    while True:
        print("  0. EXIT: ")
        print("  1. Encrypt a text")
        print("  2. Decrypt a text")
        print("  3. Encrypt a text into an image")
        print("  4. Decrypt an image")
        print("  s. Symbols list")
        opt = input("\nType an option: ")

        if opt == "0":
            return

        elif opt == "1":
            txt = input("Text to encrypt: ")
            pwd = input("Password: ")
            enc_txt = encrypt(txt,pwd)
            if enc_txt != -1:
                print(f"\nEncrypted text: {Fore.GREEN}{enc_txt}\n")
            else:
                print("\n"+Fore.RED+"Invalid text"+"\n")

        elif opt == "2":
            txt = input("Text to decrypt: ")
            pwd = input("Password: ")
            dec_txt = decrypt(txt,pwd)
            if dec_txt != -1:
                print(f"\nDecrypted text: {Fore.LIGHTCYAN_EX}{dec_txt}\n")
            else:
                print(f"\n{Fore.RED} Invalid text\n")

        elif opt == "3":
            txt = input("Text to encrypt: ")
            pwd = input("Password: ")
            img_path = input("Path to the image: ")
            img_path = img_path if img_path != "" else "img.png"
            enc_txt = encrypt_toimg(txt,pwd,img_path)
            if enc_txt != -1:
                print(f"\nEncrypted text: {Fore.LIGHTCYAN_EX}{enc_txt}\n")
                print(f"\nImage saved in {Fore.LIGHTMAGENTA_EX}{img_path}\n")
            else:
                print(f"\n{Fore.RED} Invalid text\n")

        elif opt == "4":
            img_path = input("Path to the image to decrypt: ")
            pwd = input("Password: ")
            dec_txt = decrypt_img(img_path,pwd)
            if dec_txt != -1:
                print(f"\nDecrypted text: {Fore.LIGHTCYAN_EX}{dec_txt}\n")
            else:
                print(f"\n{Fore.RED} Invalid text\n")

        elif opt == "s":
            baseList = ""
            for x in BASE:
                baseList += Back.BLUE+" "+x+" "
                baseList += Back.RESET+" "
            print("\n"+baseList+"\n")

##################################################################################################################################
menu()