"""Determine uncompressed and compressed VI-CBF size

Used to compare the full and smart serialization algorithms.
However, you'll have to switch them our manually in the VI-CBF 
implementation. The last version of pyVICBF that still had the smart
algorithm is commit 3eebf08 in the pyVICBF repository:
https://github.com/malexmave/pyVICBF/blob/3eebf080d271d77d5dadd13141447392637bdd3c/vicbf/vicbf.py"""

from vicbf.vicbf import VICBF
from zlib import compress

v = VICBF(10000, 3)
for i in range(10000):
    v.insert(i)
    if i % 10 == 0:
        x = v.serialize().tobytes()
        y = compress(x, 6)
        print i, len(x), len(y), v.FPR()
