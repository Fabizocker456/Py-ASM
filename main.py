#!/usr/bin/env python
from dis import *
import sys
import lib

with open(sys.argv[1], "r") as fi:
    doc = fi.read()
co = lib.parse(doc)
exec(co)
