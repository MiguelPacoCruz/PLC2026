import re
from itertools import product

regex = re.compile(r'^1*(0+(((10)?0?)*|1))*$')

for n in range(20):
    for bits in product("01", repeat=n):
        s = "".join(bits)

        if bool(regex.fullmatch(s)) != ("011" not in s):
            print("Primeiro contraexemplo:", repr(s))
            raise SystemExit