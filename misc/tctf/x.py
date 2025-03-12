#!/usr/bin/env python3

import re

tctf = open('tctf').read()

chunks = tctf.split('\x1b[32m')
flag = [' ' for i in range(100)]

for i, chunk in enumerate(chunks[:-1]):
    num = ''
    chunk = chunk[:-1]
    while chunk[-1] in "0123456789":
        num = chunk[-1] + num
        chunk = chunk[:-1]
    flag[int(num)] = chunks[i+1][0]

print(''.join(flag))