#!/usr/bin/env python3

letters = "abcdefghijklmnopqrstuvwxyz"
letters_upper = letters.upper()

password = open("password.txt").read().strip()

assert(len(password) < 50)

ct = ''
pt = open("plaintext.txt").read()

key_idx = 0

for c in pt:
    shift = ord(password[key_idx]) - ord('a')
    if c in letters:
        ct += letters[(ord(c) - ord('a') + shift) % len(letters)]
    elif c in letters_upper:
        ct += letters_upper[(ord(c) - ord('A') + shift) % len(letters_upper)]
    else:
        ct += c
    key_idx += 1
    key_idx %= len(password)

open("ciphertext.txt", "w").write(ct)

