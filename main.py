import random
import hashlib
from colorama import init, Fore, Back; init(autoreset=True)

############################################################################
BASE = "0123456789abcdefghijklmnopqrstuvwxyz .,'"; 
BASE_LEN = len(BASE)
HEX_SYMB = "0123456789abcdef"
MAX_LEN = 94
TXT_MAX_LEN = 126
HASH_ITERS = 100
ITERS_TOADD = 10
ENC_CODE_POS = 0
TEXT_LEN_POS = [1,2]
ENC_LIST_LEN = 256

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
    # If the text has any strange symbol or its length is more than the max, return -1
    if not all(c in BASE for c in txt) or len(txt) > MAX_LEN: return -1

    # Encode the password to sha512 and get the hash (length = 128)
    hash = hashlib.sha512(pwd.encode()).hexdigest()

    # Initial number of iterations for the hash
    iters = HASH_ITERS

    # Combine 3 consecutive hashes, created from the initial hash
    hash = h2h(hash, iters)
    
    # Add ITERS_TOADD to the iterations count
    iters += ITERS_TOADD

    while True:
        # Convert each pair of hex digits from the hash to an integer
        pwd_indexes = [int(hash[i : i+2], 16) for i in range(0, len(hash), 2)]

        # Remove the duplicates from the list
        pwd_indexes = list(dict.fromkeys(pwd_indexes))

        # If the list has more than the required length (TXT_MAX_LEN + ENC_CODE_POS + TEXT_LEN_POS), break (end the loop)
        if len(pwd_indexes) >= (TXT_MAX_LEN + 3): 
            break

        # If the list doesn't have enough indexes, add other hash to the hash
        hash += h2h(hash, iters)

        # Increase the iterations count by ITERS_TOADD
        iters += ITERS_TOADD

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
    txt_indexes = pwd_indexes[3:]

    # Encrypt the length of the text (converted to hexadecimal - in string) and adding a 0 to the left if the length is less than 2 (f -> 0f)
    txt_len_enc = enc(format(len(txt_enc), 'x').rjust(2,"0"), encryption_code)

    # Save the two indexes where the text length will be saved
    txt_len_indexes = [pwd_indexes[TEXT_LEN_POS[0]] , pwd_indexes[TEXT_LEN_POS[1]]]

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
    # If the text has any strange symbol or its length is more than the max, return -1
    if not all(c in BASE for c in txt) or len(txt) > ENC_LIST_LEN: return -1

    # Encode the password to sha512 and get the hash (length = 128)
    hash = hashlib.sha512(pwd.encode()).hexdigest()

    # Initial number of iterations for the hash
    iters = HASH_ITERS

    # Combine 3 consecutive hashes, created from the initial hash
    hash = h2h(hash, iters)
    
    # Add ITERS_TOADD to the iterations count
    iters += ITERS_TOADD

    while True:
        # Convert each pair of hex digits from the hash to an integer
        pwd_indexes = [int(hash[i : i+2], 16) for i in range(0, len(hash), 2)]

        # Remove the duplicates from the list
        pwd_indexes = list(dict.fromkeys(pwd_indexes))

        # If the list has more than the required length (TXT_MAX_LEN + ENC_CODE_POS + TEXT_LEN_POS), break (end the loop)
        if len(pwd_indexes) >= (TXT_MAX_LEN + 3): 
            break

        # If the list doesn't have enough indexes, add other hash to the hash
        hash += h2h(hash, iters)

        # Increase the iterations count by ITERS_TOADD
        iters += ITERS_TOADD

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
    txt_indexes = pwd_indexes[3:]

    # Save the two indexes where the text length will be saved
    txt_len_indexes = [pwd_indexes[TEXT_LEN_POS[0]] , pwd_indexes[TEXT_LEN_POS[1]]]

    # Get the text length from the text in the txt_len_indexes, decrypt it and convert it to integer
    txt_len = int(dec(txt[txt_len_indexes[0]]+txt[txt_len_indexes[1]], encryption_code), 16)

    toret = ""
    for x in range(txt_len):
        toret += txt[txt_indexes[x]]
    toret = h2t(dec(toret, encryption_code))

    return toret

##########################################################################################################
def menu():
    print("\nThis algorithm helps you encrypt a text with a maximum length of " + str(MAX_LEN) + ", written with 40 different characters and symbols")

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
            enc_txt = encrypt(txt,pwd)
            if enc_txt != -1:
                print("\nEncrypted text: " + Fore.GREEN+enc_txt+"\n")
            else:
                print("\n"+Fore.RED+"Invalid text"+"\n")
        elif opt == "2":
            txt = input("Type the text to decrypt: ")
            pwd = input("Type the password: ")
            dec_txt = decrypt(txt,pwd)
            if dec_txt != -1:
                print("\nDecrypted text: " + Fore.LIGHTCYAN_EX+dec_txt+"\n")
            else:
                print("\n"+Fore.RED+"Invalid text"+"\n")
        elif opt == "s":
            baseList = ""
            for x in BASE:
                baseList += Back.BLUE+" "+x+" "
                baseList += Back.RESET+" "
            print("\n"+baseList+"\n")

##################################################################################################################################
menu()