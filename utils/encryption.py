import random
from colorama import Fore, init; init()

from utils.colortext import colortext
from utils.cryptography import *
from constants.constants import *

def encrypt_txt(text:str, pwd:str) -> str:
    hash = get_pwd_hash(pwd)
    print(colortext("Preparing...", Fore.MAGENTA))
    if len(text)>TXT_MAX_LEN or len(text)==0: 
        raise Exception(f"text length ({len(text)}) is invalid. It must be between 1 and {TXT_MAX_LEN} characters.")

    # Seed the random generator with the hash
    seed = int(hash,16)
    random.seed(seed) 

    # Get the encryption code
    encryption_code = get_encryption_code(hash) 

    print(colortext("Creating the random base...", Fore.MAGENTA))
    # Fill the ciphertext with random characters
    ciphertext = [random.choice(HEX_SYMB) for _ in range(CIPHER_LEN)]  

    print(colortext("Encrypting the input and its length...", Fore.MAGENTA))
    # INFO: Encrypt the text and the text length
    textE = enc(t2h(text), encryption_code)
    textE_len = len(textE)
    textE_len_max_digits = len(format(CIPHER_LEN,"x")) # If the position length is 5, the length of the encrypted text will fit in 5 digits
    textE_len_fixed_len = format(textE_len,"x").rjust(textE_len_max_digits,"0")
    textE_lenE = enc(textE_len_fixed_len, encryption_code) # Encrypted text length (fixed length)

    print(colortext("Generating the length indexes...", Fore.MAGENTA))
    # Get the indexes where the INFO will be stored
    textE_len_idxs = get_textE_len_idxs(seed, CIPHER_LEN, textE_len_max_digits)

    print(colortext("Generating the encrypted text indexes...", Fore.MAGENTA))
    textE_idxs = get_textE_idxs(seed, CIPHER_LEN, len(textE), textE_len_idxs)

    print(colortext("Creating the ciphertext...", Fore.MAGENTA))
    # Save the text and text length in toret
    for i,idx in enumerate(textE_len_idxs):
        ciphertext[idx] = textE_lenE[i]
    for i,idx in enumerate(textE_idxs):
        ciphertext[idx] = textE[i]

    return "".join(ciphertext)


def decrypt_cipher(ciphertext:str, pwd:str) -> str:
    hash = get_pwd_hash(pwd)
    print(colortext("Preparing...", Fore.MAGENTA))
    cipher_len = len(ciphertext) # Same as CIPHER_LEN

    if not all(c in HEX_SYMB for c in ciphertext) or len(ciphertext) != cipher_len: 
        raise Exception("Encrypted text is invalid")

    # Seed the random generator with the hash
    seed = int(hash,16)
    random.seed(seed) 

    # Get the encryption code
    encryption_code = get_encryption_code(hash)  

    print(colortext("Decrypting the text length...", Fore.MAGENTA))
    # Decrypt the text length
    textE_len_digits = len(format(cipher_len,"x")) # If the position length is 5, the length of the encrypted text will fit in 5 digits
    textE_len_idxs = get_textE_len_idxs(seed, cipher_len, textE_len_digits)
    textE_lenE = "".join([ciphertext[idx] for idx in textE_len_idxs])
    textE_len = int(dec(textE_lenE, encryption_code), 16)

    print(colortext("Decrypting the text...", Fore.MAGENTA))
    # Decrypt the text
    textE_idxs = get_textE_idxs(seed, cipher_len, textE_len, textE_len_idxs)
    textE = "".join([ciphertext[idx] for idx in textE_idxs])
    text = h2t(dec(textE, encryption_code))

    return text


def get_img_arr(text:str) -> np.ndarray:
    img_arr = np.array(
            [[int(text[i:i+2], 16), 
            int(text[i+2:i+4], 16), 
            int(text[i+4:i+6], 16)] 
            for i in range(0, len(text), 6)], 
        dtype=np.uint8)
    return img_arr.reshape(IMG_SIZE, IMG_SIZE, 3)