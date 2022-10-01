import os
from colorama import Fore, init; init()
from PIL import Image
import time

from .Text import Text
from .Options import Options
from .Encryptor import Encryptor
from .Decryptor import Decryptor
from .ImageCreator import ImageCreator

import sys; sys.path.append("..")
from constants.constants import *

class Menu():
    def __init__(self):
        self.create_folders()
        print(f'\n{Text("Max length of the text",Fore.CYAN)}: {Text(f"{TXT_MAX_LEN:,}",Fore.GREEN)} (you can change it in {Text("config.py",Fore.LIGHTYELLOW_EX)}')
        option = Options(["EXIT", "Encrypt", "Decrypt text", "Decrypt image"]).get_choice()
        
        if option == 0: 
            exit()

        elif option == 1: 
            self.encrypt()

        elif option == 2:
            self.decrypt_text()

        elif option == 3:
            self.decrypt_image()

    
    def create_folders(self):
        if not os.path.exists(INPUT_DIR): os.mkdir(INPUT_DIR)
        if not os.path.exists(OUTPUT_DIR): os.mkdir(OUTPUT_DIR)


    def encrypt(self):
        text = open(self.get_input_file("Text filename: ", "txt")).read()
        pwd = input("Password: ")
        enc_text_file = self.get_file("New text filename: ", "txt")
        enc_img_file = self.get_file("New image filename: ", "png") if self.yes_no("Save image? [y/n]: ") else None

        t1 = time.time()
        try:
            encrypted_text = Encryptor(text, pwd).encrypt()
            self.save_text(encrypted_text, enc_text_file)
            print(Text("\nText encrypted succesfully\n", Fore.GREEN))
            if enc_img_file:
                self.save_img(encrypted_text, enc_img_file)
                print(Text("Image saved", Fore.GREEN))
        except Exception as e:
            print(Text(f"Error: {e}", Fore.RED))
            return

        print(Text(f"\nDone in {time.time() - t1:.2f} seconds", Fore.LIGHTYELLOW_EX))


    def decrypt(self, ciphertext:str) -> str:
        pwd = input("Password: ")
        dec_text_file = self.get_file("New filename: ", "txt")

        t1 = time.time()
        try:
            decypted_text = Decryptor(ciphertext, pwd).decrypt()
            self.save_text(decypted_text, dec_text_file)
            print(Text("\nText decrypted succesfully\n", Fore.GREEN))
        except Exception as e:
            print(Text(f"Error: {e}", Fore.RED))
            return

        print(Text(f"\nDone in {time.time() - t1:.2f} seconds", Fore.LIGHTYELLOW_EX))


    def decrypt_text(self):
        ciphertext = open(self.get_input_file("Ciphertext filename: ", "txt")).read()
        self.decrypt(ciphertext)


    def decrypt_image(self):
        ciphertext = self.img_to_text(self.get_input_file("Cipher image filename: ", "png"))
        self.decrypt(ciphertext)


    def img_to_text(self, img_file:str) -> str:
        img_arr = np.array(Image.open(img_file)).flatten()
        img_str = "".join([f'{n:02x}' for n in img_arr])
        return img_str


    def yes_no(self, msg:str="Save? [y/n]: ") -> bool:
        inp = input(msg)
        if inp.lower() == "y": return True
        elif inp.lower() == "n": return False
        else: return self.yes_no(msg)


    def save_text(self, text:str, file:str):
        with open(f"{OUTPUT_DIR}/{file}", "w") as f:
            f.write(text)


    def save_img(self, text:str, file:str):
        img_arr = ImageCreator(text).get_img_arr()
        Image.fromarray(img_arr).save(f"{OUTPUT_DIR}/{file}")


    def get_file(self, msg:str, ext:str) -> str:
        while True:
            filename = input(msg)
            if "." in filename:
                if filename.endswith(f".{ext}"): return filename
                print(Text("Invalid extension", Fore.RED))
                continue
            return f"{filename}.{ext}"


    def get_input_file(self, msg:str, ext:str) -> str:
        while True:
            file = self.get_file(msg, ext)
            path = f"{INPUT_DIR}/{file}"
            if os.path.exists(path): return path
            print(Text("File not found",Fore.RED))