import random
from colorama import Fore, init; init()

import sys; sys.path.append("..")
from constants.constants import *
from utils.cryptography import *
from .Text import Text

class Encryptor:
    def __init__(self, text:str, pwd:str):
        self.text = text
        self.pwd = pwd
        self.hash = get_pwd_hash(self.pwd)


    def encrypt(self) -> str: # Returns a ciphertext
        print(Text("Preparing...", Fore.MAGENTA))
        if len(self.text)>TXT_MAX_LEN or len(self.text)==0: 
            raise Exception(f"Text length ({len(self.text)}) is invalid. It must be between 1 and {TXT_MAX_LEN} characters.")

        # Seed the random generator with the hash
        seed = int(self.hash,16)
        random.seed(seed) 

        # Get the encryption code
        encryption_code = get_encryption_code(self.hash) 

        print(Text("Creating the random base...", Fore.MAGENTA))
        # Fill the ciphertext with random characters
        ciphertext = [random.choice(HEX_SYMB) for _ in range(CIPHER_LEN)]  

        print(Text("Encrypting the input and its length...", Fore.MAGENTA))
        # INFO: Encrypt the text and the text length
        textE = enc(t2h(self.text), encryption_code)
        textE_len = len(textE)
        textE_len_max_digits = len(format(CIPHER_LEN,"x")) # If the position length is 5, the length of the encrypted text will fit in 5 digits
        textE_len_fixed_len = format(textE_len,"x").rjust(textE_len_max_digits,"0")
        textE_lenE = enc(textE_len_fixed_len, encryption_code) # Encrypted text length (fixed length)

        print(Text("Generating the length indexes...", Fore.MAGENTA))
        # Get the indexes where the INFO will be stored
        textE_len_idxs = get_textE_len_idxs(seed, CIPHER_LEN, textE_len_max_digits)

        print(Text("Generating the encrypted text indexes...", Fore.MAGENTA))
        textE_idxs = get_textE_idxs(seed, CIPHER_LEN, len(textE), textE_len_idxs)

        print(Text("Creating the ciphertext...", Fore.MAGENTA))
        # Save the text and text length in toret
        for i,idx in enumerate(textE_len_idxs):
            ciphertext[idx] = textE_lenE[i]
        for i,idx in enumerate(textE_idxs):
            ciphertext[idx] = textE[i]

        return "".join(ciphertext)