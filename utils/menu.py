import os
from colorama import Fore, init; init()
from PIL import Image
import time

from classes.Options import Options
from utils.colortext import colortext
from utils.encryption import encrypt_txt, decrypt_cipher, get_img_arr
from constants.constants import *

def menu():
    create_folders()
    print(f'\n{colortext("Max length of the text",Fore.CYAN)}: {colortext(f"{TXT_MAX_LEN:,}",Fore.GREEN)} (you can change it in {colortext("config.py",Fore.LIGHTYELLOW_EX)}')
    option = Options(["EXIT", "Encrypt", "Decrypt text", "Decrypt image"]).get_choice()
    
    if option == 0: 
        exit()

    elif option == 1: 
        encrypt()

    elif option == 2:
        decrypt_colortext()

    elif option == 3:
        decrypt_image()


def create_folders():
    if not os.path.exists(INPUT_DIR): os.mkdir(INPUT_DIR)
    if not os.path.exists(OUTPUT_DIR): os.mkdir(OUTPUT_DIR)


def encrypt():
    text = open(get_input_file("text filename: ", "txt")).read()
    pwd = input("Password: ")
    enc_text_file = get_file("New text filename: ", "txt")
    enc_img_file = get_file("New image filename: ", "png") if yes_no("Save image? [y/n]: ") else None

    t1 = time.time()
    try:
        encrypted_text = encrypt_txt(text, pwd)
        save_colortext(encrypted_text, enc_text_file)
        print(colortext("\ntext encrypted succesfully\n", Fore.GREEN))
        if enc_img_file:
            save_img(encrypted_text, enc_img_file)
            print(colortext("Image saved", Fore.GREEN))
    except Exception as e:
        print(colortext(f"Error: {e}", Fore.RED))
        return

    print(colortext(f"\nDone in {time.time() - t1:.2f} seconds", Fore.LIGHTYELLOW_EX))


def decrypt(ciphertext:str) -> str:
    pwd = input("Password: ")
    dec_text_file = get_file("New filename: ", "txt")

    t1 = time.time()
    try:
        decypted_text = decrypt_cipher(ciphertext, pwd)
        save_colortext(decypted_text, dec_text_file)
        print(colortext("\ntext decrypted succesfully\n", Fore.GREEN))
    except Exception as e:
        print(colortext(f"Error: {e}", Fore.RED))
        return

    print(colortext(f"\nDone in {time.time() - t1:.2f} seconds", Fore.LIGHTYELLOW_EX))


def decrypt_colortext():
    ciphertext = open(get_input_file("Ciphertext filename: ", "txt")).read()
    decrypt(ciphertext)


def decrypt_image():
    ciphertext = img_to_colortext(get_input_file("Cipher image filename: ", "png"))
    decrypt(ciphertext)


def img_to_colortext(img_file:str) -> str:
    img_arr = np.array(Image.open(img_file)).flatten()
    img_str = "".join([f'{n:02x}' for n in img_arr])
    return img_str


def yes_no(msg:str="Save? [y/n]: ") -> bool:
    inp = input(msg)
    if inp.lower() == "y": return True
    elif inp.lower() == "n": return False
    else: return yes_no(msg)


def save_colortext(text:str, file:str):
    with open(f"{OUTPUT_DIR}/{file}", "w") as f:
        f.write(text)


def save_img(text:str, file:str):
    img_arr = get_img_arr(text)
    Image.fromarray(img_arr).save(f"{OUTPUT_DIR}/{file}")


def get_file(msg:str, ext:str) -> str:
    while True:
        filename = input(msg)
        if "." in filename:
            if filename.endswith(f".{ext}"): return filename
            print(colortext("Invalid extension", Fore.RED))
            continue
        return f"{filename}.{ext}"


def get_input_file(msg:str, ext:str) -> str:
    while True:
        file = get_file(msg, ext)
        path = f"{INPUT_DIR}/{file}"
        if os.path.exists(path): return path
        print(colortext("File not found",Fore.RED))