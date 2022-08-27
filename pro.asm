.code
  load_global print_fun @ name: "print"
  load_const helo
  call_function 1
  @ stack:
  @ 0: "Hello, World"
  @ 1: print
  @ call_function: calls indexed element with element at 0
  @ pop(top) -> stack
  @ => print("Hello World")
  @    stack << None


  return_value 0 @ None
.data
  const helo marshal fa0d48656c6c6f2c20576f726c6421 @ str "Hello, World!"
  name print_fun print
.meta
  stacksize 4
  firstlineno 1
