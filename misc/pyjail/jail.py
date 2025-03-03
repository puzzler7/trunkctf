#!/usr/bin/env python3

while True:
    inp = input(">>> ")
    if any(c not in "abcdefghijklmnopqrstuvwxyz " for c in inp):
        print("Jailbreak detected - exiting")
        exit(1)
    exec(inp)