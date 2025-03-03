#!/usr/bin/env python3

import re

flag = open("flag.txt").read()
assert flag.startswith('tctf{') and flag.endswith('}')

while True:
    rx = input("Enter flag regex: ")

    if re.fullmatch(rx, flag):
        print("Nope!")
    else:
        print("Nope!")