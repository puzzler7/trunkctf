"Jormungandr" is a reversing challenge that I wrote for [ImaginaryCTF 2022](https://2022.imaginaryctf.org/Challenges.html) with the exact same description and attachment. Googling the challenge description in quotes or `jormungandr "ictf"` pulls up [this Japanese writeup](https://nanimokangaeteinai-hateblo-jp.translate.goog/entry/2022/07/21/200947?_x_tr_sl=ja&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=sc#Reversing-474-Jormungandr-18-solves) for the challenge, which contains the flag.

Alternatively, you could just reverse the script (although this would be much harder!). I seem to have lost my solve script, but I still have the following notes on the challenge itself:

> The challenge is both a python interpreter for an esolang, and the esolang source. It reads the source, splits it by spaces, and treats every word as an instruction. The pseudocode is something like:
```
write false to "hile"
write true to "hile"
many no-ops
read user input to "flag"
delete previous instruction
modify user input
if "hile":
    jump to top
if user input matches expected value
    print "not"
print "bad"
quit by deleting every instruction
```