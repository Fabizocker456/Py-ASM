#!/usr/bin/python
import dis
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
    # stage III
    consts = ([], {}) # ([const], {name: index_of_const})
    names = ([], {}) # ^
    flags = 0
    cellvars = []
    freevars = ([], {}) # ^^^^
    locs = ([], {}, [0, 0, 0]) # (*^^^^^, [argc, posargc, kwargc])
    for i, line in modes["data"]:
        typ = i[0]
        cur_name = i[1]
        if typ == "const":
            sub = i[2]
            if sub == "marshal":
                item = marshal.loads(bytes.fromhex(i[3]))
            elif sub == "pickle":
                item = pickle.loads(bytes.fromhex(i[3]))
            if item not in consts[0]:
                consts[0].append(item)
            consts[1][cur_name] = consts[0].index(item)
        elif typ == "name":
            act_name = i[2]
            if act_name not in names[0]:
                names[0].append(act_name)
            names[1][cur_name] = names[0].index(act_name)
        elif typ == "flag":
            cmpfln = dis.COMPILER_FLAG_NAMES
            actflag = {cmpfln[o]: o for o in cmpfln}[act_name.upper()]
            if len(i) <= 2 or i[2] not in ["xor", "not"]:
                flags |= actflag
            elif i[2] == "xor":
                flags ^= actflag
            else:
                flags &= ~actflag
        elif typ == "cell":
            cellvars.append(cur_name)
        elif typ == "free":
            act_var = i[2]
            if act_var not in freevars[0]:
                freevars[0].append(act_var)
            freevars[1][cur_name] = freevars[0].index(act_var)
        elif typ == "local":
            act_var = i[2]
            if act_var not in locs[0]:
                locs[0].append(act_var)
            locs[1][cur_name] = locs[0].index(act_var)
            if len(i) <= 4:
                argt = i[3]
                if argt == "posonly":
                    locs[2][0] += 1
                    locs[2][1] += 1
                elif argt == "kwonly":
                    locs[2][2] += 1
                elif argt == "":
                    locs[2][0] += 1

    ops = []
    anchors = {}
    for addr, (i, line) in enumerate(modes["code"]):
        if i[0].startswith(":"):
            anchors[i.pop(0)[1:]] = addr
    for addr, (i, line) in enumerate(modes["code"]):
        print(i)
        op = i[0]
        if op.isdigit() and 0 <= int(op) <= 255:
            op = int(op)
        else:
            op = dis.opmap[i[0].upper()]
        if op < dis.HAVE_ARGUMENT:
            ops.append([op, 0])
            continue
        arg = i[1]
        print(addr)
        if arg.isdigit() and 0 <= int(arg) <= 255:
            ops.append([op, int(arg)])
            continue
        elif op in dis.hascompare:
            arg = dis.cmp_op.index(arg)
        elif op in dis.hasname:
            arg = names[1][arg]
        elif op in dis.hasfree:
            arg = freevars[1][arg]
        elif op in dis.hasconst:
            arg = consts[1][arg]
        elif op in dis.haslocal:
            arg = locs[1][arg]
        elif op in dis.hasjabs:
            arg = anchors[arg]
        elif op in dis.hasjrel:
            assert(anchors[arg] > addr)
            arg = anchors[arg] - addr
        ops.append([op, int(arg)])
    print(ops)
    bytecode = b''
    for i in ops:
        bytecode += bytes(i)
    crp = {
        "code": bytecode,
        "argcount": locs[2][0],
        "posonlyargcount": locs[2][1],
        "kwonlyargcount": locs[2][2],
        "nlocals": len(locs[0]),
        "varnames": tuple(locs[0]),
        "cellvars": tuple(cellvars),
        "freevars": tuple(freevars[0]),
        "names": tuple(names[0]),
        "consts": tuple(consts[0]),
        "flags": flags,
        "stacksize": 0,
        "firstlineno": 1,
        "linetable": b"\x02\x00" * (len(bytecode) // 2),
        "filename": "<asm>",
        "name": "<asm>"
    }
    for i, line in modes["meta"]:
        allow = {
                "name": str,
                "filename": str,
                "stacksize": int,
                "firstlineno": int,
                "linetable": bytes
        }
        tp = allow[i[0]]
        if tp == bytes:
            val = bytes.fromhex(i[1])
        else:
            val = tp(i[1])
        crp[i[0]] = val
    for i in crp:
        code = code.replace(**{f"co_{i}": crp[i]})
    return code
