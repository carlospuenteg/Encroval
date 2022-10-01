import numpy as np

import sys; sys.path.append("..")
from config import *

INPUT_DIR = "input"
OUTPUT_DIR = "output"

HEX_SYMB = "0123456789abcdef"

IMG_SIZE = int(np.sqrt((16**POS_LEN)//6))                   # Size that the image will have (the image is a square)
CIPHER_LEN = (IMG_SIZE**2)*6                                # Length that the ciphertext will have
TXT_E_MAX_LEN = CIPHER_LEN - len(format(CIPHER_LEN,"x"))    # Max length text (encrypted) can have
TXT_MAX_LEN = TXT_E_MAX_LEN//2                              # Max length the input text can have (Because the encrypted text is twice the length of the input text)