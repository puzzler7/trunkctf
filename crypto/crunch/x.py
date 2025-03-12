#!/usr/bin/env python3

header = b"P6\n2000 2000\n255\n"

f = open("out.enc", "rb")
out = open("out.ppm", "wb")
out.write(header)
out.write(f.read())