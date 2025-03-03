#!/usr/bin/env python3

from Crypto.Util.number import long_to_bytes

# factored at https://www.alpertron.com.ar/ECM.HTM
p = 52205281475604429596898144467
q = 72208538205556556793711585497 

n = 3769667061963016434087725644476865647177314490119927995099
e = 65537
c = 155385042393016593007021191989408776894222769009913957569

phi = (p-1)*(q-1)
d = pow(e, -1, phi)
m = pow(c, d, n)

print(long_to_bytes(m))