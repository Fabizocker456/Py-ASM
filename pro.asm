.code
  :init load_global print_fun @ name: "print"
  load_const helo
  call_function 1
  return_value 0

.void

== explanation ==

---
stack << x: push onto stack
<< stack: pop top
<<= stack: pop at arg
---

1. stack << global "print"
stack is now
0 print

2. stack << const "Hello, World!"
stack is now
0 "Hello, World!"
1 print

3. stack << (<<= stack).__call__(<< stack)
stack is now
0 None

4. return (<< stack)
stack is empty
stop execution

.data
  const helo marshal fa0d48656c6c6f2c20576f726c6421 @ str "Hello, World!"
  name print_fun print
.meta
  stacksize 4 @ 2 too much
  firstlineno 69 @ because why not
