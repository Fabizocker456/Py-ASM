#!/usr/bin/python
import dis, marshal, pickle, readline
print("""
Choose:
1) Print all bytecode instructions
2) Marshal any object
3) Pickle any object
4) Compile and disassemble input
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
        if arg:
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
    print("enter \"end\" to stop")
    ls = []
    while 1:
        c = input(">>> ")
        if c == "end":
            break
        ls.append(c)
    ls = "\n".join(ls)
    c = compile(ls, "<asm>", "exec")
    dis.dis(c)
