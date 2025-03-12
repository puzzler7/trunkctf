#!/usr/bin/env python3

from random import randint, choice

flag = "tctf{i_wonder_if_this_flag_counts_as_flaky?_adc7a5330fc}"
fake = "jctf{red_flags_and_fake_flags_form_an_equivalence_class}"

red = "\x1b[31m"
green = "\x1b[32m"
clear = '\x1b\x5b\x48\x1b\x5b\x32\x4a\x1b\x5b\x33\x4a'

def set_pos(n):
    return f'\x1b[1;{n+1}{choice("Hf")}'

to_real = set(range(len(flag)))
to_fake = set()

out = clear

while len(to_real) + len(to_fake) > 0:
    if choice([0,1]) and len(to_real) > 0:
        pos = choice(list(to_real))
        out += set_pos(pos)
        if choice([0,1]):
            out += red + choice(fake)
        else:
            out += green + flag[pos]
            to_real.remove(pos)
            to_fake.add(pos)
    elif len(to_fake) > 0:
        pos = choice(list(to_fake))
        out += set_pos(pos)
        if choice([0,1]):
            out += red + choice(fake)
        else:
            out += red + fake[pos]
            to_fake.remove(pos)

out += '\x1b[0m\n'
open("jctf", 'w').write(out)
