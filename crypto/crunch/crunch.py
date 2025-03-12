#!/usr/bin/env python3

import secrets
from Crypto.Cipher import AES
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

SIZE = 2000
FONT_SIZE = 275
NUM_CHUNKS = 4

flag = open("flag.txt").read()
assert len(flag) % NUM_CHUNKS == 0
flag_chunks = [flag[i*len(flag)//NUM_CHUNKS:(i+1)*len(flag)//NUM_CHUNKS] for i in range(NUM_CHUNKS)]
img = Image.new(mode='RGB', size=(SIZE, SIZE))

draw = ImageDraw.Draw(img)
font = ImageFont.truetype("LiberationMono-Regular.ttf", FONT_SIZE)

for i, chunk in enumerate(flag_chunks):
    draw.text((FONT_SIZE, (SIZE//(NUM_CHUNKS+1) * (i+1)) - FONT_SIZE/2), chunk, (255, 255, 255), font=font)


img.save("flag.ppm")

flag_bytes = open("flag.ppm", "rb").read()
while len(flag_bytes) % 16 != 0:
    flag_bytes += b'\x00'
key = secrets.token_bytes(16)
cipher = AES.new(key, AES.MODE_ECB)
ct = cipher.encrypt(flag_bytes)
open("out.enc", "wb").write(ct)