import random

import sys; sys.path.append("..")
from constants.constants import *
from utils.cryptography import *

class Encryptor:
    def __init__(self, text:str, pwd:str):
        self.text = text
        self.pwd = pwd
        self.hash = get_pwd_hash(self.pwd)


    def encrypt(self) -> str: # Returns a ciphertext
        if len(self.text)>TXT_MAX_LEN or len(self.text)==0: 
            raise Exception("Text length is invalid")

        # Seed the random generator with the hash
        seed = int(self.hash,16)
        random.seed(seed) 

        # Get the encryption code
        encryption_code = get_encryption_code(self.hash) 

        # Fill the ciphertext with random characters
        ciphertext = [random.choice(HEX_SYMB) for _ in range(CIPHER_LEN)]  

        # INFO: Encrypt the text
        textE = enc(t2h(self.text), encryption_code)

        # INFO: Encrypt the text length
        textE_len = len(textE)
        textE_len_max_digits = len(format(CIPHER_LEN,"x")) # If the position length is 5, the length of the encrypted text will fit in 5 digits
        textE_len_fixed_len = format(textE_len,"x").rjust(textE_len_max_digits,"0")
        textE_lenE = enc(textE_len_fixed_len, encryption_code) # Encrypted text length (fixed length)

        # Get the indexes where the INFO will be stored
        textE_len_idxs = get_textE_len_idxs(seed, CIPHER_LEN, textE_len_max_digits)
        textE_idxs = get_textE_idxs(seed, CIPHER_LEN, len(textE), textE_len_idxs)

        # Save the text and text length in toret
        for i,idx in enumerate(textE_len_idxs):
            ciphertext[idx] = textE_lenE[i]
        for i,idx in enumerate(textE_idxs):
            ciphertext[idx] = textE[i]

        return "".join(ciphertext)