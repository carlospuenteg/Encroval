import numpy as np

import sys; sys.path.append("..")
from config import *

INPUT_DIR = "input"
OUTPUT_DIR = "output"

HEX_SYMB = "0123456789abcdef"

IMG_SIZE = int(np.sqrt((16**POS_LEN)//6))   # Size that the image will have (the image is a square)
ENC_LEN = (IMG_SIZE**2)*6              # Length that the encrypted text will have
TXT_MAX_LEN = ENC_LEN//2-1-POS_LEN     # Max length text (not encrypted) can have