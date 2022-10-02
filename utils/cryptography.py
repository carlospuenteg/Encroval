import hashlib
import random

from constants.constants import *

def enc(txt, encryption_code:str) -> str:
    encTxt = ""
    for x in txt:
        encTxt += encryption_code[int(x,16)]  # The symbol in the equivalent position
    return encTxt


# Decrypt an encrypted text with an encryption code
def dec(txt:str, encryption:str) -> str:
    decTxt = ""
    for x in txt:
        decTxt += HEX_SYMB[encryption.index(x)]  # The symbol in the equivalent position
    return decTxt


# Encode the password to sha512 and get a hash (length = 128)
def get_pwd_hash(pwd:str) -> str:
    return hashlib.sha512(pwd.encode()).hexdigest()


def get_encryption_code(hash:str) -> str:
    encryption_code = ""
    while len(encryption_code) < 16: # While the encryption string doesn't have 16 symbols
        if (hash[0] not in encryption_code):
            encryption_code += hash[0]
        hash = h2h(hash)
    return encryption_code


def get_textE_len_idxs(seed:int, encryption_len:int, textE_len_digits:int) -> tuple: # Save txt_len_enc in the first POS_LEN indexes
    random.seed(seed)
    return random.sample(range(encryption_len), textE_len_digits)

def get_textE_idxs(seed:int, encryption_len:int, textE_len:int, textE_len_idxs:tuple) -> tuple:
    random.seed(seed)

    return random.sample([x for x in range(encryption_len) if x not in textE_len_idxs], textE_len)


# Create a new hash from a hash
def h2h(hash:str, iters:int=1) -> str:
    for _ in range(iters):
        hash = hashlib.sha512(hash.encode()).hexdigest()
    return hash

# Convert from text to hexadecimal
def t2h(txt:str) -> str:
    return txt.encode('utf-8').hex()

# Convert hexadecimal to utf-8
def h2t(hex:str)-> str:
    return bytes.fromhex(hex).decode('utf-8')