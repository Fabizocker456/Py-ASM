#!/usr/bin/python
import dis, opcode
import types
import marshal, pickle

import sys

def process_input(code: str, modec: list[str], comment = "@"):
    c = map(lambda i: (i[0] + 1, i[1]), enumerate(code.split("\n")))
    c = map(lambda i: (i[0], i[1].split(comment)[0]), c)
    c = map(lambda i: (i[0], i[1].strip()), c)
    c = filter(lambda i: bool(i[1]), c)
    c = list(c)
    mode = "void"
    modes = {i: [] for i in modec}
    for line, i in c:
        if i.startswith("."):
            mode = i[1:]
            if mode not in modec:
                raise SyntaxError(f"invalid mode: {mode} (line {line})")
        elif mode in modes:
            modes[mode].append((list(filter(bool, i.split())), line))
    return modes

def procure_data(inp: list, out: dict):
    for i, line in inp:
        typ = i[0]
        name = i[1]
        if typ == "const":
            sub = i[2]
            if sub == "marshal":
                val = marshal.loads(bytes.fromhex(i[3]))
            elif sub == "pickle":
                val = pickle.loads(bytes.fromhex(i[3]))
            else:
                raise SyntaxError(f"invalid 'const' type: {sub} (line {line})")
            if val not in out["const"][0]:
                out["const"][0].append(val)
            out["const"][1][name] = out["const"][0].index(val)
        elif typ == "name":
            act_name = i[2]
            if act_name not in out["names"][0]:
                out["names"][0].append(act_name)
            out["names"][1][name] = out["names"][0].index(act_name)
        elif typ == "cell":
            if name not in out["cell"]:
                out["cell"].append(name)
        elif typ == "free":
            act_name = i[2]
            if act_name not in out["free"][0]:
                out["free"][0].append(act_name)
            out["free"][1][name] = out["free"][0].index(act_name)
        else:
            raise SyntaxError("invalid '.data' directive: {typ} (line {line})")

def create_bytecode(code: list, data: dict):
    marks = {}
    for lno, (i, line) in enumerate(code):
        while i[0].startswith(":"):
            marks[i.pop(0)[1:]] = lno
    instr = []
    for lno, (i, line) in enumerate(code):
        op = i[0]
        if op.isdigit():
            op = int(op)
        else:
            op = dis.opmap[op.upper()]
        if opcode.is_pseudo(op):
            raise SyntaxError("opcode {op} ({dis.opname[op].lower()}) is a pseudo-opcode (line {line})")
        if op >= 256:
            raise SyntaxError("opcode {op} too big (line {line})")
        if op < dis.HAVE_ARGUMENT:
            instr.append([op, 0])
            continue
        arg = i[1]
        if arg.isdigit():
            instr.append([op, int(arg)])
            continue
        if op == dis.BINARY_OP:
            for l, i in enumerate(dis._nb_ops):
                if arg == i[1] or arg.upper() == i[0] or arg.upper() == i[0][3:]:
                    arg = l
                    break
                else:
                    raise SyntaxError(f"bad binary operation: {arg} (line {line})")
        if op in dis.hasjrel:
            if arg.startswith(":"):
                arg = arg[1:]
            nm = f":{arg}"
            arg = marks[arg] - lno + 1
            if ((arg > 1) if (bw := dis._is_backward_jump(op)) else (arg < 1)):
                raise SyntaxError(f"a {'backward' if bw else 'forward'} jump can never reach {nm} (delta {arg - 1}) (line {line})")
            arg = arg + lno - 1
        elif op in dis.hasname:
            arg = data["names"][1][arg]
        elif op in dis.hasconst:
            arg = data["const"][1][arg]
        elif op in dis.hasfree:
            arg = data["free"][1][arg]
        else:
            arg = int(arg)
            
def parse(inp:str) -> types.CodeType:
    code = compile("...", "<assembly>", "exec")
    modes = process_input(inp, ["data", "code", "meta", "void"], comment="@")
    data = {
        "const": ([], {}),
        "vars": ([], {}, 0, 0, 0),
        "flags": 0,
        "free": ([], {}),
        "cell": [],
        "names": ([], {})
    }
    procure_data(modes["data"], data)
    byc = create_bytecode(modes["code"], data)


    sys.exit(0)
