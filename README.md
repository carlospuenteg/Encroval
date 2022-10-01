# Encroval

## Index
* [Description](#description)
* [Get Started](#get-started)
  * [Install requirements](#install-requirements)
  * [Enter the input](#enter-the-input)
  * [Run](#run)
* [Configuration](#configuration)
* [Examples](#examples)
  * [Encryption](#encryption-example)
  * [Text Decryption](#text-decryption-example)
  * [Image Decryption](#image-decryption-example)

## Description

Encroval is an encryption tool that allows you to encrypt a text into other text or image using a password.

It can encrypt a text of any length and the password can be up to 2<sup>128</sup> bits long and accepts any UTF-8 character (1,112,064 different characters).




## Get Started

### Install Requirements

```bash
pip3 install -r requirements.txt
```


### Enter the input

#### Select the text to encrypt
Place the text you want to encrypt (a `.txt` file) in the `input` folder.

#### Select the text/image to decrypt
Place the text you want to encrypt (a `.txt` file) or the image (a `.png` file) in the `input` folder.


### Run

```bash
python3 main.py
```




## Configuration

You can change the `POS_LEN` in the `config.py` file, which changes the input text's maximum length.

Default is `POS_LEN = 4`, so the maximum length the text can have by default is **32,446**

The more the `POS_LEN` is, the longer the text can be, but the longer it will take to encrypt and decrypt it.

| POS_LEN | Max text lenght |
|-|-|
| 1 | 2 |
| 2 | 107 |
| 3 | 2,026 |
| 4 | 32,446 |
| 5 | 524,169 |
| 6 | 8,386,749 |
| 7 | 134,188,028 |
| 8 | 2,147,329,544 |
| ... | ... |




## Examples

### Encryption example

<img width=400 src=readme-assets/example_encryption.png>

#### `config.py`

```python
POS_LEN = 2
```

#### Input text (`input/test.txt`)
```txt
This is a test 123!!!

It can have every UTF-8 character! ✔️ ❤️ ☆
```

#### Password
```txt
test#@–{}password123¿?
```

#### Encrypted text (`output/encrypted_text.txt`)
```txt
3e8b00b4bcbb4ff246fdb3bc9afd63cf080e1cbefdc4b4bb2b5f1400f3fd4e6cb10d40825d0ab41e080e4e751a1ebbb8e7c4448fc14434d5c84d7fb3cc68e2c66033d5cfeece84bd256888b5e3dbb5bdc7fd47845be373e44bc8defbabb92e544f5eb0b4c43403084344d663
```

#### Encrypted image (`output/encrypted_image.png`)
<img width=70 src=readme-assets/encrypted_image.png>



### Text Decryption example

<img width=400 src=readme-assets/example_text_decryption.png>

#### Input text (`input/encrypted_text.txt`)
```txt
This is a test 123!!!

It can have every UTF-8 character! ✔️ ❤️ ☆
```

#### Password
```txt
test#@–{}password123¿?
```

#### Decrypted text (`output/decrypted_text.txt`)
```txt
This is a test 123!!!

The text can have every UTF-8 character! ✔️ ❤️ ☆
```



### Image Decryption example

<img width=400 src=readme-assets/example_image_decryption.png>

#### Input image (`input/encrypted_image.png`)
<img width=70 src=readme-assets/encrypted_image.png>

#### Password
```txt
test#@–{}password123¿?
```

#### Decrypted image (`output/decrypted_image.txt`)
```txt
This is a test 123!!!

The text can have every UTF-8 character! ✔️ ❤️ ☆
```
