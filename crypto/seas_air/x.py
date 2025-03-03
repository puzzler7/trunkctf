#!/usr/bin/env python3

ct = 'jsjv{ryw_dkcruhi_cuqdi_yj_xqi_je_ru_iuskhu_hywxj?}'

letters = "abcdefghijklmnopqrstuvwxyz"
diff = (ord(ct[0]) - ord('t')) % 26
enc_letters = letters[-diff:] + letters[:-diff]

dec_map = dict(zip(letters, enc_letters))

print(''.join(dec_map.get(c, c) for c in ct))