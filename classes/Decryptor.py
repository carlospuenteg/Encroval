import random

import sys; sys.path.append("..")
from constants.constants import *
from utils.cryptography import *
from .Text import Text
from colorama import Fore, init; init()

class Decryptor:
    def __init__(self, ciphertext:str, pwd:str):
        self.ciphertext = ciphertext
        self.pwd = pwd
        self.hash = get_pwd_hash(pwd)


    def decrypt(self) -> str:
        print(Text("Preparing...", Fore.MAGENTA))
        cipher_len = len(self.ciphertext) # Same as CIPHER_LEN

        if not all(c in HEX_SYMB for c in self.ciphertext) or len(self.ciphertext) != cipher_len: 
            raise Exception("Encrypted text is invalid")

        # Seed the random generator with the hash
        seed = int(self.hash,16)
        random.seed(seed) 

        # Get the encryption code
        encryption_code = get_encryption_code(self.hash)  

        print(Text("Decrypting the text length...", Fore.MAGENTA))
        # Decrypt the text length
        textE_len_digits = len(format(cipher_len,"x")) # If the position length is 5, the length of the encrypted text will fit in 5 digits
        textE_len_idxs = get_textE_len_idxs(seed, cipher_len, textE_len_digits)
        textE_lenE = "".join([self.ciphertext[idx] for idx in textE_len_idxs])
        textE_len = int(dec(textE_lenE, encryption_code), 16)

        print(Text("Decrypting the text...", Fore.MAGENTA))
        # Decrypt the text
        textE_idxs = get_textE_idxs(seed, cipher_len, textE_len, textE_len_idxs)
        textE = "".join([self.ciphertext[idx] for idx in textE_idxs])
        text = h2t(dec(textE, encryption_code))

        return text