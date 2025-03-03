The guides I found most helpful when re-learning how do to pwn to write this challenge were [this one](https://www.ired.team/offensive-security/code-injection-process-injection/binary-exploitation/rop-chaining-return-oriented-programming) and [this one](https://codearcana.com/posts/2013/05/28/introduction-to-return-oriented-programming-rop.html), but there's many around.

The exploit is fairly simple - the name is a 64 character buffer, but we're reading 128 characters into it, causing a stack buffer overflow. The information for where the program wants to return to, so we simply tell it to return to the code that prints the flag.

The exact layout of the payload:
- 64 characters to fill the name buffer
- 8 characters to fill $rbp - this isn't important, it's just more filler before we overwrite the return address
- an 8 byte little-endian pointer to a ROP gadget - specifically, this is pointing to the assembly instruction `ret`, which immediately returns to the next thing on the stack
- an 8 byte little-endian pointer to the flag function.

See `x.py` for the full code.