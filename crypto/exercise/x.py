#!/usr/bin/env python3

ct = bytes.fromhex('616b7fcf8e3d747163c885234a7c63cc86354a6e67c892234a6979ccaa247a6754d98735716168dd9432796d54cfc066763a69c8c52d')
key = []
known = b"tctf{"
for i in range(5):
    key.append(ct[i] ^ known[i])
key.append(ct[-1] ^ b'}'[0])

key *= 100
pt = bytes(key[i] ^ c for i, c in enumerate(ct))
print(pt)
