#!/usr/bin/python
from dis import *
import sys
import lib

with open(sys.argv[1], "r") as fi:
    doc = fi.read()
co = lib.parse(doc)
dis(co)
print(list(co.co_code))
exec(co)
