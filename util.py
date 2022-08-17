#!/usr/bin/python
import dis, marshal
print("""
Choose:
1) Print all bytecode instructions
2) Marshal any object

        """)
inp = input("> ")
if inp == "1":
    for i in dis.opmap:
        print(f"{i} [{dis.opmap[i]}]")
