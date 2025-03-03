#!/usr/bin/env python3

import secrets

pt = open("flag.txt", "rb").read()
key = secrets.token_bytes(6) * 100
ct = bytes(key[i] ^ c for i, c in enumerate(pt))

print(ct.hex())

# Output:
# 616b7fcf8e3d747163c885234a7c63cc86354a6e67c892234a6979ccaa247a6754d98735716168dd9432796d54cfc066763a69c8c52d