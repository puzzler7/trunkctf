#!/usr/bin/env python3

import secrets

def rot_one(c):
    return ((c&1) << 7 )+ (c >> 1)

def rot(a):
    return [rot_one(i) for i in a]

def unrot_one(c):
    return ((c<<1) & 0b11111111) + (c >> 7)

def unrot(a):
    return [unrot(i) for i in a]

flag = b"tctf{xors_and_more_xors_i_snore_abce274c}"
rand = secrets.token_bytes(len(flag))
rand_orig = rand

ans = []

for i in range(len(flag)):
    val = (flag[i] ^ rand[i])
    for j in range(i):
        val = unrot_one(val)
    ans.append(val)
    rand = rot(rand)

print("rand", '{' + ", ".join(hex(i) for i in rand_orig) + '};')
print("ans", '{' + ", ".join(hex(i) for i in ans) + '};')

print()
print(len(rand))

rand = rand_orig

# test I generated the arrays correctly
for i, c in enumerate(flag):
    if c^rand[i]^ans[i]:
        print("bad char", i, c, rand[i], ans[i], c^rand[i]^ans[i])
    rand = rot(rand)
    ans = rot(ans)


