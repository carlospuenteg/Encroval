import numpy as np

import sys; sys.path.append("..")
from constants.constants import *

class ImageCreator:
    def __init__(self, text:str):
        self.text = text


    def get_img_arr(self) -> np.ndarray:
        img_arr = np.array(
                [[int(self.text[i:i+2], 16), 
                int(self.text[i+2:i+4], 16), 
                int(self.text[i+4:i+6], 16)] 
                for i in range(0, len(self.text), 6)], 
            dtype=np.uint8)
        return img_arr.reshape(IMG_SIZE, IMG_SIZE, 3)