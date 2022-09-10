#!/usr/bin/env python
import dis, marshal, pickle, readline
import types

def pr_co(co):
    for i in map(lambda i: i[3:], filter(lambda i: i.startswith("co_"), dir(co))):
        j = getattr(co, "co_" + i)
        t = type(j)
        if t == bytes:
            j = list(j)
        elif i == "flags":
            j = dis.pretty_flags(j)
        print(f"{i}: ({t.__name__}) {j}")

print("""
Choose:
1) Print all bytecode instructions
2) Marshal any object
3) Pickle any object
4) Compile and disassemble code
5) Compile and disassemble a function
""")
inp = input("> ")
if inp == "1":
    ls = []
    for i in dis.opmap:
        op = dis.opmap[i]
        cur = f"{i} [{op:3}]"
        
        ls.append(cur)
    maxlen = max(map(len, ls))
    for i in ls:
        print(i.rjust(maxlen))
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
elif inp == "5":
    print("enter \"::\" to stop")
    ls = []
    while 1:
        c = input(">>> " if ls else ">>> def func(")
        if c == "::":
            break
        ls.append(c)
    ls = "\n".join(ls)
    ls = "def func("+ls
    print(ls)
    exec(ls)
    c = func
    try:
        dis.dis(c, show_caches = True)
    except:
        dis.dis(c)
    pr_co(c.__code__)
    
else:
    print("Invalid input!")
