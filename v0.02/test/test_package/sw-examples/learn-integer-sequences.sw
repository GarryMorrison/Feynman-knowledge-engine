fib |0> => |0>
fib |1> => |1>
fib |*> !=> arithmetic( fib minus[1] |_self>, |+>, fib minus[2] |_self>)

fact |0> => |1>
fact |*> !=> arithmetic(|_self>, |*>, fact minus[1] |_self>)

-- provide a literal operator wrapper around the function operator
-- function operators (currently?) don't get invoked in x.apply_op(context, op)
-- only literal operators do.
is-prime |*> #=> is-prime |_self>

seq |count> => sp2seq range(|1>, |100>)
seq |fib> => fib sp2seq range(|1>, |30>)
seq |fact> => fact sp2seq range(|1>, |30>)
seq |primes> => such-that[is-prime] sp2seq range(|1>, |200>)

