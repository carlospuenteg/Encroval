import random

import sys; sys.path.append("..")
from constants.constants import *
from utils.cryptography import *

class Encryptor:
    def __init__(self, text:str, pwd:str):
        self.text = text
        self.pwd = pwd
        self.hash = get_pwd_hash(self.pwd)


    def encrypt(self) -> str: 
        if len(self.text)>TXT_MAX_LEN or len(self.text)==0: 
            raise Exception("Text length is invalid")

        # Seed the random generator with the hash
        seed = int(self.hash,16)
        random.seed(seed) 

        # Get the encryption code
        encryption_code = get_encryption_code(self.hash) 

        # Fill the encrypted text with random characters
        ciphertext = [random.choice(HEX_SYMB) for _ in range(ENC_LEN)]  

        # INFO: Encrypt the text and text length
        textE = enc(t2h(self.text), encryption_code)
        textE_len_digits = len(format(ENC_LEN,"x")) # If the position length is 5, the length of the encrypted text will fit in 5 digits
        textE_len = len(textE)
        textE_len_fixed_len = format(textE_len,"x").rjust(textE_len_digits,"0")
        textE_lenE = enc(textE_len_fixed_len, encryption_code) # Encrypted text length (fixed length)

        # Get the indexes where the INFO will be stored
        textE_len_idxs = get_textE_len_idxs(seed, ENC_LEN, textE_len_digits)
        textE_idxs = get_textE_idxs(seed, ENC_LEN, len(textE), textE_len_idxs)

        # Save the text and text length in toret
        for i,idx in enumerate(textE_len_idxs):
            ciphertext[idx] = textE_lenE[i]
        for i,idx in enumerate(textE_idxs):
            ciphertext[idx] = textE[i]

        return "".join(ciphertext)