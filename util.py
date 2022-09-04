#!/usr/bin/env python
import dis, marshal, pickle, readline

def pr_co(co):
    for i in map(lambda i: i[3:], filter(lambda i: i.startswith("co_"), dir(co))):
        j = getattr(co, "co_" + i)
        t = type(j)
        if t == bytes:
            j = list(j)
        print(f"{i}: ({t.__name__})")

print("""
Choose:
1) Print all bytecode instructions
2) Marshal any object
3) Pickle any object
4) Compile and disassemble code
""")
inp = input("> ")
if inp == "1":
    maxlen = max(map(len, dis.opmap.keys()))
    for i in dis.opmap:
        op = dis.opmap[i]
        arg = ""
        if op < dis.HAVE_ARGUMENT:
            arg = "no argument"
        elif op in dis.hasjrel:
            arg = "relative jump"
        elif op in dis.hasjabs:
            arg = "absolute jump"
        elif op in dis.hasfree:
            arg = "free variable"
        elif op in dis.hasname:
            arg = "name"
        elif op in dis.haslocal:
            arg = "local variable"
        elif op in dis.hascompare:
            arg = "comparison"
        else:
            arg = "???"
        arg = f" ({arg})"
        i = i.lower()
        i = i.ljust(maxlen)
        sop = f"{op}".rjust(3, "0")
        print(f"[{sop}] {i}{arg}")
        

elif inp == "2":
    c = eval(input(">>> "))
    print(marshal.dumps(c).hex())
elif inp == "3":
    c = eval(input(">>> "))
    print(pickle.dumps(c).hex())
elif inp == "4":
    print("enter \"::\" to stop")
    ls = []
    while 1:
        c = input(">>> ")
        if c == "::":
            break
        ls.append(c)
    ls = "\n".join(ls)
    c = compile(ls, "<asm>", "exec")
    try:
        dis.dis(c, show_caches = True)
    except:
        dis.dis(c)
    pr_co(c)
else:
    print("Invalid input!")
