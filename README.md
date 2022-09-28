# Encroval

## Description

Encroval is an encryption tool that allows you to encrypt and decrypt files using a password.

It can encrypt a text of any length with a password and the only way to decrypt it is by knowing it.

The password can be up to 2<sup>128</sup> bits long and accepts any UTF-8 character (1,112,064 different characters).


## Config

In `config.py` you can change `HEX_POS_LEN`, which is **the length that the positions in the encryption will have (in hex)**
| HEX_POS_LEN | Hex positions range | Max length of the text to encrypt |
|-|-|-|
| 1 | 0x0 - 0xF | 1 |
| 2 | 0x00 - 0xFF | 105 |
| 3 | 0x000 - 0xFFF | 2,024 |
| 4 | 0x0000 - 0xFFFF | 32,443 |
| 5 | 0x00000 - 0xFFFFF | 524,166 |
| 6 | 0x000000 - 0xFFFFFF | 8,386,745 |
| 7 | 0x0000000 - 0xFFFFFFF | 134,188,024 |
| 8 | 0x00000000 - 0xFFFFFFFF | 2,147,329,539 |

`HEX_POS_LEN` affects the maximum length of the message that can be encrypted.

But the max length of the text isn't equal to the number of bits that a position has, because some bits are used to store other things

## Encrypt a text

| Input | Description |
|-|-|
| Text path | Path of the text file to encrypt (within the `input` folder) |
| Password | Password to encrypt the text |
| New filename | Name that the encrypted text will have (within the `output` folder) |
| Image filename | Name that the encrypted image will have (within the `output` folder) |

|||
|-|-|
| Text to encrypt | hello world
| Password | test#@–{}password123¿?
| Encrypted text |    70c15441e9d300393879a961b87440e60dfe8bbdcca9160fd52a68b45993eac8414365c952c405e2609d4dc9556b9f192d261d8069c121e0db458fd15bdd2ba0a263d5e5bfa9e202dd4827c655236f6e9a5ee69dcb52dc93d0202c4bd4ba3e394feb61919fa7993ac49ae6a88b26255a772483bb06f0624311eafd7b2ec8cc38d5f9f8ee56894a2c0994208647f67596a434f3

If you run it again, you will create a different encrypted text:
|||
|-|-|
| Text to encrypt | hello world
| Password | test#@–{}password123¿?
| Encrypted text |    d00b2b23f9b1cc8e7faf0d0148614eafcdc4a68c16992e1d47c90c88d7380408e5b5b3c6be86b5f1e9236c9055abb1532cceebc169b3966dfbbcb7e19b7857703d1914138f5c81bb4d57acbd9c7963b942e3e3facb2d8c07cf86e276dae5ad3ff3787a37052253befbabc77e6983d2a8c731377652e90f0efc8e2e0e9efb35c565e2367cb2b64a47283dda3c5ebcf722cf5afe

## Encrypt a text into an image

<img src=readme-assets/img-res.jpg width=200>


## Decrypt a text

|||
|-|-|
| Text to decrypt | 70c15441e9d300393879a961b87440e60dfe8bbdcca9160fd52a68b45993eac8414365c952c405e2609d4dc9556b9f192d261d8069c121e0db458fd15bdd2ba0a263d5e5bfa9e202dd4827c655236f6e9a5ee69dcb52dc93d0202c4bd4ba3e394feb61919fa7993ac49ae6a88b26255a772483bb06f0624311eafd7b2ec8cc38d5f9f8ee56894a2c0994208647f67596a434f3
| Password | test#@–{}password123¿?
| Decrypted text | hello world

|||
|-|-|
| Text to decrypt | d00b2b23f9b1cc8e7faf0d0148614eafcdc4a68c16992e1d47c90c88d7380408e5b5b3c6be86b5f1e9236c9055abb1532cceebc169b3966dfbbcb7e19b7857703d1914138f5c81bb4d57acbd9c7963b942e3e3facb2d8c07cf86e276dae5ad3ff3787a37052253befbabc77e6983d2a8c731377652e90f0efc8e2e0e9efb35c565e2367cb2b64a47283dda3c5ebcf722cf5afe
| Password | test#@–{}password123¿?
| Decrypted text | hello world


## Decrypt an image

|||
|-|-|
| Image path | img.png
| Password | test#@–{}password123¿?
| Decrypted text | hello world
