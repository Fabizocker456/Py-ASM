.code
  resume 0
  :init push_null
  load_name print_fun
  load_const helo
  call 1
  pop_top
  jump_backward :init
.data
  name print_fun print
  name ell Ellipsis
  const helo marshal fa0d48656c6c6f2c20576f726c6421
.meta
  stacksize 16
  firstlineno 69 @ because why not
