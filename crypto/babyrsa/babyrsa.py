#!/usr/bin/env python3

# pip install pycryptodome
from Crypto.Util.number import bytes_to_long, getPrime

m = bytes_to_long(open("flag.txt", "rb").read())
e = 65537
p = getPrime(96)
q = getPrime(96)
n = p*q

assert m < n

c = pow(m, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{c = }")
