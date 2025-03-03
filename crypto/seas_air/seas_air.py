#!/usr/bin/env python3

from random import randint

letters = "abcdefghijklmnopqrstuvwxyz" * 2**16
key = randint(0, 2**16)
enc_map = {}

for i in range(26):
    enc_map[letters[i]] = letters[i+key]

flag = open("flag.txt", "r").read()
enc_flag = ''.join(enc_map.get(c, c) for c in flag)

print(enc_flag)

# Output:
# jsjv{ryw_dkcruhi_cuqdi_yj_xqi_je_ru_iuskhu_hywxj?}