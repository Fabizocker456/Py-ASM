#!/usr/bin/python
from dis import *
import sys
import types, typing
import regex as re
import marshal, pickle
import builtins

def parse(inp:str, code:types.CodeType = None) -> types.CodeType:
    if not code:
        code = compile("...", "<assembly>", "exec")
    # stage I
    inp = inp.split("\n")
    # stage II
    mode = "void"
    modes = {"data":[], "code":[], "meta":[]}
    for line, i in enumerate(inp):
        i = i.strip()
        if i.startswith("@"):
            continue
        if "@" in i:
            i = i.split("@")[0]
        i = i.strip()
        i = i.split(" ")
        i = list(filter(bool, map(lambda o: o.strip(), i)))
        if not i:
            continue
        if i[0].startswith("."):
            mode = i[0][1:]
            continue
        if mode in modes:
            modes[mode].append((i, line))
    print(modes)
    # stage III
    code_da
