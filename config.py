POS_LEN = 4
"""
The length that the positions in the encryption will have (in hex)

1 = 0x0 - 0xF               Max text length: 2
2 = 0x00 - 0xFF             Max text length: 107
3 = 0x000 - 0xFFF           Max text length: 2,026
4 = 0x0000 - 0xFFFF         Max text length: 32,446
5 = 0x00000 - 0xFFFFF       Max text length: 524,169
6 = 0x000000 - 0xFFFFFF     Max text length: 8,386,749
7 = 0x0000000 - 0xFFFFFFF   Max text length: 134,188,028
8 = 0x00000000 - 0xFFFFFFFF Max text length: 2,147,329,544
...
"""