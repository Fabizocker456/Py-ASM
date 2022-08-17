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
        if g := re.fullmatch("\\.([a-z_]+)\\s*(?:@.*)?", i.strip()):
            mode = g.group(1)
        else:
            if mode in modes and i.strip():
                if re.fullmatch("\\s*(?:@.*)?", i.strip()):
                    continue
                if "@" in i:
                    i = i.split("@")[0]
                modes[mode].append((i.strip(), line))
    # stage III
    consts = [None]
    const_names = {}
    names = []
    name_names = {}
    for c, line in modes["data"]:
        if i := re.fullmatch("const\\s+(.+)", c):
            i = i.group(1)
            if g := re.fullmatch("marshal\\s+([a-z_]+)\\s+([0-9a-f]+)", i):
                obj = marshal.loads(bytes.fromhex(g.group(2)))
                name = g.group(1)
            else:
                raise SyntaxError(f"Could not extract data directive: \"{i}\" (line {line})")
            consts.append(obj)
            const_names[name] = len(consts) - 1
        elif i := re.fullmatch("name\\s+([a-z_]+)\\s+(\\S+)", c):
            obj = i.group(2)
            name = i.group(1)
            if obj not in names:
                names.append(obj)
            name_names[name] = names.index(obj)
    instrs = []
    for i, line in modes["code"]:
        if g := re.fullmatch("([a-z_]+)\\s+(\\S+)", i):
            op = g.group(1)
            arg = g.group(2)
            op = op.upper()
        else:
            raise SyntaxError(f"Could not extract instruction: \"{i}\" (line {line})")
        if op not in opmap:
            raise NameError(f"No such operation: \"{op}\" (line {line})")
        op = opmap[op]
        if op in hasjrel or op in hasjabs:
            try:
                arg = int(arg)
            except:
                raise ValueError(f"Jump target {arg} invalid: must be int (line {line})")
        elif op in hasconst:
            if arg not in const_names:
                raise NameError(f"No registered constant: \"{arg}\" (line {line})")
            arg = const_names[arg]
        elif op in hasname:
            if arg not in name_names:
                raise NameError(f"No name registered for {arg}")
            arg = name_names[arg]
        elif op in hascompare:
            if arg not in cmp_op:
                    raise ValueError(f"No comparative operator: \"{arg}\" (line {line})")
            else:
                arg = cmp_op.index(arg)
        else:
            try:
                arg = int(arg)
            except:
                raise ValueError(f"Argument {arg} not int (line {line})")
            if arg > 255 or arg < 0:
                raise ValufError(f"Argument {arg} too large (>255) or too small (<0) (line {line})")
        instrs.append((op, arg, line))
    meta = {}
    for i, line in modes["meta"]:
        if g := re.fullmatch("([a-z]+)\\s+([a-zA-Z0-9]+)", i):
            meta[g.group(1)] = g.group(2)
        else:
            raise SyntaxError("Bad meta directive: \"{i}\" (line {line})")

    # stage IV
    prg = b""
    for op, arg, line in instrs:
        prg += bytes((op, arg))
    code = code.replace(co_code = prg)
    code = code.replace(co_consts = tuple(consts))
    code = code.replace(co_names = tuple(names))
    code = code.replace(co_linetable = bytes((2, 1) * (len(prg) // 2)))
    typemap = {
        "name": str,
        "argcount": int,
        "posonlyargcount": int,
        "kwonlyargcount": int,
        "nlocals": int,
        "varnames": (str,),
        "cellvars": (str,),
        "freevars": (str,),
        "filename": str,
        "firstlineno": int,
        "stacksize": int,
        "flags": int
    }
    for i in meta:
        if i in typemap:
            j = meta[i]
            t = typemap[i]
            if t in (str, int):
                code = code.replace(**{f"co_{i}": t(j)})
            elif t == (str,):
                code = code.replace(**{f"co_{i}": tuple(j.split(":"))})
    return code
