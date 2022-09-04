.code
  :init load_global print_fun @ name: "print"
  load_const helo
  store_name a
  load_global a
  call_function 1
  pop_top
  jump_absolute init

.data
  const helo marshal fa0d48656c6c6f2c20576f726c6421 @ str "Hello, World!"
  name print_fun print
.meta
  stacksize 4 @ 2 too much
  firstlineno 69 @ because why not
.data
  name a vara
