# Encroval

## Index
* [Description](#description)
* [Get Started](#get-started)
  * [Install requirements](#install-requirements)
  * [Enter the input](#enter-the-input)
  * [Run](#run)
* [Configuration](#configuration)

## Description

Encroval is an encryption tool that allows you to encrypt a text into other text or image using a password.

It can encrypt a text of any length and the password can be up to 2<sup>128</sup> bits long and accepts any UTF-8 character (1,112,064 different characters).




## Get Started

#### Install Requirements

```bash
pip3 install -r requirements.txt
```


#### Enter the input

##### Select the text to encrypt
Place the text you want to encrypt (a `.txt` file) in the `input` folder.

##### Select the text/image to decrypt
Place the text you want to encrypt (a `.txt` file) or the image (a `.png` file) in the `input` folder.


#### Run

```bash
python3 main.py
```




## Configuration

You can change the `POS_LEN` in the `config.py` file, which changes the input text's maximum length.

Default is `POS_LEN = 4`, so the maximum length the text can have by default is **32,446**

The more the `POS_LEN` is, the longer the text can be, but the longer it will take to encrypt and decrypt it.