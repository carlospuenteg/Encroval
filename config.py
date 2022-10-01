POS_LEN = 4
"""
The length that the positions in the encryption will have (in hex)
1 = 0x0 - 0xF               Max text length: 1
2 = 0x00 - 0xFF             Max text length: 105
3 = 0x000 - 0xFFF           Max text length: 2,024
4 = 0x0000 - 0xFFFF         Max text length: 32,443
5 = 0x00000 - 0xFFFFF       Max text length: 524,166
6 = 0x000000 - 0xFFFFFF     Max text length: 8,386,745
7 = 0x0000000 - 0xFFFFFFF   Max text length: 134,188,024
8 = 0x00000000 - 0xFFFFFFFF Max text length: 2,147,329,539
...

This affects the maximum length of the message that can be encrypted
Max text length isn't equal to the number of bits that a position can have, because those bits are also used to store other things
"""