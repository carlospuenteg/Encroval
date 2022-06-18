import random
import hashlib
from colorama import init, Fore, Back; init(autoreset=True)
from PIL import Image
import numpy as np
import random
import os

############################################################################
HEX_SYMB = "0123456789abcdef"
HASH_ITERS = 100
ITERS_TOADD = 10
ENC_CODE_POS = 0

HEX_POS_LEN = 6
IMG_SIZE = int(np.sqrt((16**HEX_POS_LEN)//6))
ENC_LIST_LEN = (IMG_SIZE**2)*6
TXT_MAX_LEN = ENC_LIST_LEN//2-1-HEX_POS_LEN

TEXT_LEN_POS = range(1, HEX_POS_LEN+1)
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
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
    return txt.encode('utf-8').hex()

# Convert hexadecimal to utf-8
def h2t(hex):
    return bytes.fromhex(hex).decode('utf-8')

##########################################################################################################
def encrypt(txt, pwd, new_filename=None):
    # If, for example, ENC_LIST_LEN = 200, then the text on hexadecimal can have a length of up to 197 (200-3)
    
    if len(txt) > TXT_MAX_LEN or len(txt) == 0: 
        return -1

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
    if new_filename:
        open(f"{OUTPUT_FOLDER}/{new_filename}.txt", "w").write(toret)
    return toret

def encrypt_file(txt_filename, pwd, new_filename="text-enc"):
    txt = open(f"{INPUT_FOLDER}/{txt_filename}.txt", "r").read()
    return encrypt(txt, pwd, new_filename)

##########################################################################################################
def decrypt(txt, pwd, new_filename=None):
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

    if new_filename:
        open(f"{OUTPUT_FOLDER}/{new_filename}.txt", "w").write(toret)
    return toret

def decrypt_file(txt_filename, pwd, new_filename=None):
    txt = open(f"{INPUT_FOLDER}/{txt_filename}.txt", "r").read()
    return decrypt(txt, pwd, new_filename)

##########################################################################################################
def save_hex_img(enc_text, img_filename="img"):
    img_arr = np.array([[int(enc_text[i:i+2], 16), int(enc_text[i+2:i+4], 16), int(enc_text[i+4:i+6], 16)] for i in range(0, len(enc_text), 6)], dtype=np.uint8)
    img_arr = img_arr.reshape(IMG_SIZE, IMG_SIZE, 3)
    Image.fromarray(img_arr).save(f"{OUTPUT_FOLDER}/{img_filename}.png")
    return enc_text

def decrypt_img_txt(img_filename, pwd, new_filename):
    img_arr = np.array(Image.open(f"{INPUT_FOLDER}/{img_filename}.png")).flatten()
    img_str = "".join([f'{n:02x}' for n in img_arr])
    return decrypt(img_str, pwd, new_filename)

##########################################################################################################
def menu():
    if not os.path.exists(INPUT_FOLDER): os.makedirs(INPUT_FOLDER)
    if not os.path.exists(OUTPUT_FOLDER): os.makedirs(OUTPUT_FOLDER)

    print(f"\nThis algorithm helps you encrypt a text with a maximum length of {TXT_MAX_LEN:,} characters, written with utf-8 encoding.\n")

    while True:
        print("  0. EXIT: ")
        print("  1. Encrypt a text")
        print("  2. Decrypt a text")
        print("  3. Decrypt an image")
        opt = input("\nType an option: ")

        if opt == "0":
            return

        elif opt == "1":
            txt_filename = None
            while not txt_filename or not os.path.exists(f"{INPUT_FOLDER}/{txt_filename}.txt"):
                txt_filename = input("Text filename: ")
                if not os.path.exists(f"{INPUT_FOLDER}/{txt_filename}.txt"):
                    print(f"{Fore.RED}File not found")
            pwd = input("Password: ")
            new_filename = input("Name of the new file: ")
            save_hex_img_q = input("Save an encrypted image? (y/n): ")
            if save_hex_img_q == "y":
                img_filename = input("Name of the image file: ")
                img_filename = img_filename if img_filename != "" else "img"

            enc_text = encrypt_file(txt_filename, pwd, new_filename)
                
            if enc_text == -1:
                print(f"\n{Fore.RED}Text length is invalid\n")
            else:
                if save_hex_img_q == "y":
                    save_hex_img(enc_text, img_filename)
                print(f"\n{Fore.GREEN}Text encrypted succesfully\n")
                if save_hex_img_q == "y": 
                    print(f"{Fore.MAGENTA}Image saved\n")
                
        elif opt == "2":
            txt_filename = None
            while not txt_filename or not os.path.exists(f"{INPUT_FOLDER}/{txt_filename}.txt"):
                txt_filename = input("Filename of the text to decrypt: ")
                if not os.path.exists(f"{INPUT_FOLDER}/{txt_filename}.txt"):
                    print(f"{Fore.RED}File not found")
            pwd = input("Password: ")
            new_filename = input("Name of the new file: ")
            dec_txt = decrypt_file(txt_filename, pwd, new_filename)
            if dec_txt != -1:
                print(f"\n{Fore.GREEN}Text decrypted succesfully\n")
            else:
                print(f"\n{Fore.RED} Invalid text\n")

        elif opt == "3":
            img_filename = None
            while not img_filename or not os.path.exists(f"{INPUT_FOLDER}/{img_filename}.png"):
                img_filename = input("Image filename: ")
                if not os.path.exists(f"{INPUT_FOLDER}/{img_filename}.png"):
                    print(f"{Fore.RED}File not found")
            pwd = input("Password: ")
            new_filename = input("Name of the new file: ")
            dec_txt = decrypt_img_txt(img_filename, pwd, new_filename)
            if dec_txt != -1:
                print(f"\n{Fore.GREEN}Text decrypted succesfully\n")
            else:
                print(f"\n{Fore.RED}Invalid text\n")

##################################################################################################################################
menu()