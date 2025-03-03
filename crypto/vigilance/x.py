#!/usr/bin/env python3

from collections import Counter

ct = open("ciphertext.txt").read()

def matches(s, diff):
    print("matching", diff)
    i = 0
    ret = 0
    while i+diff < len(s):
        ret += s[i] == s[i+diff]
        i += 1
    return ret

possible_key_lens = [(i, matches(ct, i)) for i in range(1, 50)]
possible_key_lens = sorted(possible_key_lens, key=lambda x: x[1], reverse=True)

print("Likely key lengths:")
for l, v in possible_key_lens[:5]:
    print(f"{l}: {v}")

key_len = possible_key_lens[0][1]
buckets = [ct[i::27].lower().replace(' ', '') for i in range(27)]

key = []
for bucket in buckets:
    e = Counter(bucket).most_common(1)[0][0]
    key.append((ord(e) - ord('e')) % 26)


print("Key:", ''.join(chr(i+ord('a')) for i in key))

letters = "abcdefghijklmnopqrstuvwxyz"
letters_upper = letters.upper()

key_idx = 0
pt = ''

for c in ct:
    shift = key[key_idx]
    if c in letters:
        pt += letters[(ord(c) - ord('a') - shift) % len(letters)]
    elif c in letters_upper:
        pt += letters_upper[(ord(c) - ord('A') - shift) % len(letters_upper)]
    else:
        pt += c
    key_idx += 1
    key_idx %= len(key)

open("recovered_plaintext.txt", "w").write(pt)