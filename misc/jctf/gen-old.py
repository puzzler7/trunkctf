#!/usr/bin/env python3

from random import randint, choice

clear = '\x1b\x5b\x48\x1b\x5b\x32\x4a\x1b\x5b\x33\x4a'

red = "\x1b[31m"
green = "\x1b[32m"

def set_pos(n):
    return f'\x1b[1;{n}{choice("Hf")}'

def shuffle_print(s, obsf=False):
    chars = list(enumerate(s))

    last_green = 0

    while len(chars) > 0:
        idx = randint(0, len(chars)-1)
        i, c = chars[idx]
        if obsf and randint(0,1):
            last_green = 0
            print(red, end='')
            print(set_pos(i+1), end=choice(s))
            continue

        if obsf and not last_green:
            last_green = 1
            print(green, end='')
        last_green = 1
        
        print(set_pos(i+1), end=c)
        chars.pop(idx)
    print()

flag = 'tctf{green_flags_may_work}'
fake = 'jctf{red_flags_and_fake_flags_form_an_equivalence_class}'

print(clear, end='')
shuffle_print(flag, obsf=1)
print(clear, end='')
print(red, end='')
shuffle_print(fake)